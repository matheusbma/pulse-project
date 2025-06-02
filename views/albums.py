import streamlit as st
from config import COLORS, apply_custom_css
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Aplica o CSS personalizado
apply_custom_css()

# Carregamento dos dados
@st.cache_data
def load_data():
    try:
        artists_df = pd.read_csv('data/artists.csv')
        albums_df = pd.read_csv('data/albums.csv')
        return artists_df, albums_df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        return None, None

# Carrega os dados
artists_df, albums_df = load_data()

if artists_df is None:
    st.stop()

# Sidebar - Seleção do artista
st.sidebar.markdown("### Procure seu artista favorito")
selected_artist = st.sidebar.selectbox(
    "Artista",
    options=sorted(artists_df['artist_name'].unique()),
    index=sorted(artists_df['artist_name'].unique()).index(st.session_state.get('selected_artist', sorted(artists_df['artist_name'].unique())[0])) if 'selected_artist' in st.session_state else 0,
    key="artist_selector_albums",
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

# Filtra os álbuns do artista selecionado
artist_albums = albums_df[albums_df['spotify_id'] == st.session_state.selected_artist_id].copy()

if not artist_albums.empty:
    # Converte release_date para inteiro para ordenação correta por ano
    artist_albums['release_year'] = pd.to_numeric(artist_albums['release_date'], errors='coerce')
    # Ordena os álbuns por ano de lançamento (mais recente primeiro)
    artist_albums = artist_albums.sort_values('release_year', ascending=False, na_position='last')

    # Layout em duas colunas para métricas
    col1, col2 = st.columns(2)
    
    with col1:
        total_albums = len(artist_albums)
        st.metric("Total de Lançamentos", total_albums)
    
    with col2:
        avg_tracks = artist_albums['total_tracks'].mean()
        st.metric("Média de Faixas/Álbum", f"{avg_tracks:.1f}")

    # 1. TIMELINE DE LANÇAMENTOS
    st.write("### 📅 Timeline de Lançamentos por Ano")
    
    # Contar álbuns por ano
    albums_per_year = artist_albums.groupby('release_year').size().reset_index(name='count')
    
    # Gráfico de linha temporal
    fig_timeline = px.line(
        albums_per_year,
        x='release_year',
        y='count',
        title=f'Lançamentos de {selected_artist} ao Longo dos Anos',
        labels={'release_year': 'Ano', 'count': 'Número de Lançamentos'},
        markers=True,
        line_shape='spline',
        height=450
    )
    fig_timeline.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    fig_timeline.update_traces(line_color='#00ff85', marker_color='#00ff85')
    st.plotly_chart(fig_timeline, use_container_width=True)

    # 2. ANÁLISE POR TIPO DE ÁLBUM
    st.write("### 🎵 Distribuição por Tipo de Álbum")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Contar álbuns por tipo
        type_counts = artist_albums['type'].value_counts()
        
        # Gráfico de barras horizontais (substituindo pizza)
        fig_bar_horizontal = px.bar(
            x=type_counts.values,
            y=type_counts.index,
            orientation='h',
            title='Tipos de Lançamentos',
            labels={'x': 'Quantidade', 'y': 'Tipo'},
            color=type_counts.values,
            color_continuous_scale=[[0, COLORS['secondary']], [0.5, COLORS['highlight']], [1, COLORS['accent2']]],
            height=400
        )
        fig_bar_horizontal.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=False
        )
        st.plotly_chart(fig_bar_horizontal, use_container_width=True)
    
    with col2:
        # Gráfico de barras verticais para tipos
        fig_bar_type = px.bar(
            x=type_counts.index,
            y=type_counts.values,
            title='Quantidade por Tipo',
            labels={'x': 'Tipo', 'y': 'Quantidade'},
            color=type_counts.values,
            color_continuous_scale='Blues',
            height=400
        )
        fig_bar_type.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=False
        )
        st.plotly_chart(fig_bar_type, use_container_width=True)

    # 3. ANÁLISE DE NÚMERO DE FAIXAS
    st.write("### 🎼 Análise do Número de Faixas por Álbum")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histograma de número de faixas
        fig_tracks = px.histogram(
            artist_albums,
            x='total_tracks',
            nbins=15,
            title='Distribuição do Número de Faixas',
            labels={'total_tracks': 'Número de Faixas', 'count': 'Quantidade de Álbuns'},
            color_discrete_sequence=['#ff6b6b'],
            height=400,
            width=500
        )
        fig_tracks.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_tracks, use_container_width=False)
    
    with col2:
        # Scatter plot: Ano vs Número de faixas
        fig_scatter = px.scatter(
            artist_albums,
            x='release_year',
            y='total_tracks',
            size='total_tracks',
            color='type',
            title='Evolução do Tamanho dos Álbuns',
            labels={'release_year': 'Ano', 'total_tracks': 'Número de Faixas'},
            hover_data=['album_name'],
            height=400,
            width=500
        )
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_scatter, use_container_width=False)

    # 4. HEATMAP DE PRODUTIVIDADE POR DÉCADA
    st.write("### 🔥 Heatmap de Produtividade por Década")
    
    # Criar década a partir do ano
    artist_albums['decade'] = (artist_albums['release_year'] // 10) * 10
    decade_type = artist_albums.groupby(['decade', 'type']).size().unstack(fill_value=0)
    
    if not decade_type.empty:
        # Criar heatmap
        fig_heatmap = px.imshow(
            decade_type.T,
            labels=dict(x="Década", y="Tipo", color="Quantidade"),
            x=decade_type.index.astype(str),
            y=decade_type.columns,
            color_continuous_scale='Viridis',
            title='Produtividade por Década e Tipo',
            height=450
        )
        fig_heatmap.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

else:
    st.info("Não há álbuns disponíveis para este artista.") 