import streamlit as st
import pandas as pd
from config import COLORS, apply_custom_css
import plotly.express as px

# Aplica o CSS personalizado
apply_custom_css()

def display_event(event):
    """Exibe os detalhes de um evento"""
    st.write(f"**Local:** {event['venue_name']}")
    st.write(f"**Cidade:** {event['venue_city']}")
    st.write(f"**País:** {event['venue_country']}")
    if pd.notna(event['start_time']):
        try:
            time = pd.to_datetime(event['start_time']).strftime('%H:%M')
            st.write(f"**Horário:** {time}")
        except:
            st.write(f"**Horário:** {event['start_time']}")
    if pd.notna(event['ticket_url']) and event['ticket_status'] in ['Tickets', 'Set Reminder']:
        st.markdown(f"[Link para Ingressos]({event['ticket_url']})")

# Carregamento dos dados
@st.cache_data
def load_data():
    try:
        artists_df = pd.read_csv('data/artists.csv')
        past_events_df = pd.read_csv('data/past_events.csv')
        future_events_df = pd.read_csv('data/future_events.csv')
        
        # Converter datas
        past_events_df['event_date'] = pd.to_datetime(past_events_df['event_date'])
        future_events_df['event_date'] = pd.to_datetime(future_events_df['event_date'])
        
        return artists_df, past_events_df, future_events_df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        return None, None, None

# Carrega os dados
artists_df, past_events_df, future_events_df = load_data()

if artists_df is None:
    st.stop()

# Sidebar - Seleção do artista
st.sidebar.markdown("### Procure seu artista favorito")
selected_artist = st.sidebar.selectbox(
    "Artista",
    options=sorted(artists_df['artist_name'].unique()),
    index=sorted(artists_df['artist_name'].unique()).index(st.session_state.get('selected_artist', sorted(artists_df['artist_name'].unique())[0])) if 'selected_artist' in st.session_state else 0,
    key="artist_selector_shows",
    label_visibility="collapsed"
)

# Atualiza o estado da sessão apenas se o artista selecionado mudou
if selected_artist != st.session_state.get('selected_artist'):
    st.session_state.selected_artist = selected_artist
    st.session_state.selected_artist_id = artists_df[artists_df['artist_name'] == selected_artist]['spotify_id'].iloc[0]
    st.rerun()

# Cabeçalho
artist_data = artists_df[artists_df['artist_name'] == selected_artist].iloc[0]

# Cabeçalho com foto e nome
col1, col2 = st.columns([1, 9])

with col1:
    image_url = artist_data['image_url'] if pd.notna(artist_data['image_url']) else 'https://via.placeholder.com/100x100?text=No+Image'
    st.markdown(f"""
    <div style='display: flex; justify-content: flex-start; margin-bottom: 1rem;'>
        <img src='{image_url}' style='border-radius: 10px; object-fit: cover; object-position: center; width: 100px; height: 100px;'>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div style='display: flex; align-items: center; margin-bottom: 2rem; margin-top: 10px;'>
            <h2 style='color: white; margin-bottom: 0;'>{selected_artist}</h2>
            <a href='{artist_data['spotify_url']}' target='_blank' style='margin-left: -20px; text-decoration: none;'>
                <img src='https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg' width='20'>
            </a>
        </div>
    """, unsafe_allow_html=True)

# Eventos futuros
future_events = future_events_df[future_events_df['spotify_id'] == st.session_state.selected_artist_id].copy()

# Eventos passados
past_events = past_events_df[past_events_df['spotify_id'] == st.session_state.selected_artist_id].copy()

# Combinar todos os eventos para análise de dados
all_events = []
if not past_events.empty:
    all_events.append(past_events)
if not future_events.empty:
    all_events.append(future_events)

# Verificar se há eventos para análise
if all_events:
    artist_events = pd.concat(all_events, ignore_index=True)
    artist_events = artist_events.sort_values('event_date')
    
    # Layout em três colunas para métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_shows = len(artist_events)
        st.metric("Total de Shows", total_shows)
    
    with col2:
        unique_countries = artist_events['venue_country'].nunique()
        st.metric("Países", unique_countries)
    
    with col3:
        unique_cities = artist_events['venue_city'].nunique()
        st.metric("Cidades", unique_cities)

    # 1. MAPA MUNDIAL DE SHOWS
    st.write("### 🗺️ Mapa Mundial dos Shows")
    
    # Dicionário básico de coordenadas para países (pode ser expandido)
    country_coords = {
        'Brazil': {'lat': -14.2350, 'lon': -51.9253},
        'United States': {'lat': 39.8283, 'lon': -98.5795},
        'United Kingdom': {'lat': 55.3781, 'lon': -3.4360},
        'Germany': {'lat': 51.1657, 'lon': 10.4515},
        'France': {'lat': 46.2276, 'lon': 2.2137},
        'Spain': {'lat': 40.4637, 'lon': -3.7492},
        'Italy': {'lat': 41.8719, 'lon': 12.5674},
        'Netherlands': {'lat': 52.1326, 'lon': 5.2913},
        'Belgium': {'lat': 50.5039, 'lon': 4.4699},
        'Switzerland': {'lat': 46.8182, 'lon': 8.2275},
        'Austria': {'lat': 47.5162, 'lon': 14.5501},
        'Portugal': {'lat': 39.3999, 'lon': -8.2245},
        'Poland': {'lat': 51.9194, 'lon': 19.1451},
        'Denmark': {'lat': 56.2639, 'lon': 9.5018},
        'Sweden': {'lat': 60.1282, 'lon': 18.6435},
        'Norway': {'lat': 60.4720, 'lon': 8.4689},
        'Australia': {'lat': -25.2744, 'lon': 133.7751},
        'Japan': {'lat': 36.2048, 'lon': 138.2529},
        'Canada': {'lat': 56.1304, 'lon': -106.3468},
        'Mexico': {'lat': 23.6345, 'lon': -102.5528},
        'Argentina': {'lat': -38.4161, 'lon': -63.6167},
        'Chile': {'lat': -35.6751, 'lon': -71.5430},
        'Colombia': {'lat': 4.5709, 'lon': -74.2973},
        'Peru': {'lat': -9.1900, 'lon': -75.0152},
        'Costa Rica': {'lat': 9.7489, 'lon': -83.7534},
        'Dominican Republic': {'lat': 18.7357, 'lon': -70.1627},
        'Puerto Rico': {'lat': 18.2208, 'lon': -66.5901}
    }
    
    # Adicionar coordenadas aos shows
    artist_events['lat'] = artist_events['venue_country'].map(lambda x: country_coords.get(x, {}).get('lat'))
    artist_events['lon'] = artist_events['venue_country'].map(lambda x: country_coords.get(x, {}).get('lon'))
    
    # Contar shows por país
    shows_by_country = artist_events.groupby('venue_country').size().reset_index(name='show_count')
    shows_by_country['lat'] = shows_by_country['venue_country'].map(lambda x: country_coords.get(x, {}).get('lat'))
    shows_by_country['lon'] = shows_by_country['venue_country'].map(lambda x: country_coords.get(x, {}).get('lon'))
    
    # Remover países sem coordenadas
    shows_by_country = shows_by_country.dropna(subset=['lat', 'lon'])
    
    if not shows_by_country.empty:
        # Mapa mundial de shows
        fig_map = px.scatter_geo(
            shows_by_country,
            lat='lat',
            lon='lon',
            size='show_count',
            hover_name='venue_country',
            color='show_count',
            title=f'Localização dos Shows de {selected_artist} pelo Mundo',
            projection='equirectangular',
            color_continuous_scale=[[0, COLORS['accent2']], [0.5, COLORS['accent']], [1, COLORS['highlight']]],
            height=600
        )
        fig_map.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            geo=dict(
                showframe=False,
                showcoastlines=True,
                coastlinecolor="rgba(0,0,0,0.3)",  # Preto suave para contornos
                showland=True,
                landcolor='rgba(15,15,25,0.8)',  # Quase preto com toque azul
                showocean=True,
                oceancolor='rgba(25,5,35,0.6)',  # Roxo muito escuro
                showlakes=True,
                lakecolor='rgba(25,5,35,0.6)',
                projection_scale=1.2
            ),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("Não foi possível gerar o mapa (coordenadas não disponíveis para os países dos shows).")

    # 2. DISTRIBUIÇÃO POR PAÍSES
    st.write("### 🌍 Distribuição de Shows por País")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top países
        country_counts = artist_events['venue_country'].value_counts().head(10)
        
        if not country_counts.empty:
            fig_countries = px.bar(
                x=country_counts.values,
                y=country_counts.index,
                orientation='h',
                title='Top 10 Países com Mais Shows',
                labels={'x': 'Número de Shows', 'y': 'País'},
                color=country_counts.values,
                color_continuous_scale=[[0, COLORS['accent2']], [0.5, COLORS['accent']], [1, COLORS['highlight']]],
                height=450
            )
            fig_countries.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                showlegend=False
            )
            st.plotly_chart(fig_countries, use_container_width=True)
        else:
            st.info("Não há dados suficientes para o gráfico de países.")
    
    with col2:
        # Top cidades
        city_counts = artist_events['venue_city'].value_counts().head(10)
        
        if not city_counts.empty:
            fig_cities = px.bar(
                x=city_counts.values,
                y=city_counts.index,
                orientation='h',
                title='Top 10 Cidades com Mais Shows',
                labels={'x': 'Número de Shows', 'y': 'Cidade'},
                color=city_counts.values,
                color_continuous_scale=[[0, COLORS['accent2']], [0.5, COLORS['accent']], [1, COLORS['highlight']]],
                height=450
            )
            fig_cities.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                showlegend=False
            )
            st.plotly_chart(fig_cities, use_container_width=True)
        else:
            st.info("Não há dados suficientes para o gráfico de cidades.")

    # 3. TIMELINE DE SHOWS
    st.write("### 📅 Timeline dos Shows")
    
    # Contar shows por mês
    artist_events['year_month'] = artist_events['event_date'].dt.to_period('M')
    shows_timeline = artist_events.groupby('year_month').size().reset_index(name='show_count')
    shows_timeline['year_month'] = shows_timeline['year_month'].astype(str)
    
    if not shows_timeline.empty:
        fig_timeline = px.line(
            shows_timeline,
            x='year_month',
            y='show_count',
            title=f'Timeline de Shows de {selected_artist}',
            labels={'year_month': 'Período', 'show_count': 'Número de Shows'},
            markers=True,
            height=450
        )
        fig_timeline.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis_tickangle=-45
        )
        fig_timeline.update_traces(line_color='#00a8b5', marker_color='#00a8b5')
        st.plotly_chart(fig_timeline, use_container_width=True)
    else:
        st.info("Não há dados suficientes para o gráfico temporal.")

else:
    st.write("### 📊 Análise de Shows")
    st.info(f"Este artista ({selected_artist}) não possui shows registrados em nossa base de dados.")
    st.write("")
    st.write("**Possíveis motivos:**")
    st.write("- Artista focado apenas em produção/estúdio")
    st.write("- Shows não catalogados em nossa base")
    st.write("- Artista em hiato ou aposentado")
    st.write("- Dados ainda não atualizados") 