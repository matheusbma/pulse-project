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
        tracks_df = pd.read_csv('data/tracks.csv')
        albums_df = pd.read_csv('data/albums.csv')
        past_events_df = pd.read_csv('data/past_events.csv')
        future_events_df = pd.read_csv('data/future_events.csv')
        return artists_df, tracks_df, albums_df, past_events_df, future_events_df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        return None, None, None, None, None

# Carrega os dados
artists_df, tracks_df, albums_df, past_events_df, future_events_df = load_data()

if artists_df is None or tracks_df is None or albums_df is None or past_events_df is None or future_events_df is None:
    st.stop()

# Sidebar - Seleção do artista
st.sidebar.markdown("### Procure seu artista favorito")
selected_artist = st.sidebar.selectbox(
    "Artista",
    options=sorted(artists_df['artist_name'].unique()),
    index=sorted(artists_df['artist_name'].unique()).index(st.session_state.get('selected_artist', sorted(artists_df['artist_name'].unique())[0])) if 'selected_artist' in st.session_state else 0,
    key="artist_selector_general",
    label_visibility="collapsed"
)

# Atualiza o estado da sessão apenas se o artista selecionado mudou
if selected_artist != st.session_state.get('selected_artist'):
    st.session_state.selected_artist = selected_artist
    st.session_state.selected_artist_id = artists_df[artists_df['artist_name'] == selected_artist]['spotify_id'].iloc[0]
    st.rerun()

artist_data = artists_df[artists_df['artist_name'] == selected_artist].iloc[0]

# Cabeçalho com foto e informações básicas
col1, col2, col3 = st.columns([1, 1.5, 1])

with col1:
    image_url = artist_data['image_url'] if pd.notna(artist_data['image_url']) else 'https://via.placeholder.com/300x300?text=No+Image'
    st.markdown(f"""
    <div style='display: flex; justify-content: flex-start; margin-bottom: 1rem;'>
        <img src='{image_url}' style='border-radius: 10px; object-fit: cover; object-position: center; width: 300px; height: 300px;'>
    </div>
    """, unsafe_allow_html=True)
    
        
with col2:
    # Cabeçalho com nome e logo do Spotify
    st.markdown(f"""
    <div style='display: flex; align-items: center;'>
        <h2 style='color: white; margin-bottom: 0;'>{selected_artist}</h2>
        <a href='{artist_data['spotify_url']}' target='_blank' style='margin-left: -20px; text-decoration: none;'>
            <img src='https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg' width='20'>
        </a>
    </div>
    """, unsafe_allow_html=True)

    # Tipo
    st.markdown(f"""
    <div style='display: flex; align-items: center; margin-bottom: 8px;'>
        <span style='color: {COLORS["accent"]}; font-weight: 500; min-width: 80px;'>Tipo:</span>
        <span style='color: white;'>{artist_data['artist_type'].title()}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Gênero (se não for grupo)
    if artist_data['artist_type'].lower() != 'banda':
        st.markdown(f"""
        <div style='display: flex; align-items: center; margin-bottom: 8px;'>
            <span style='color: {COLORS["accent"]}; font-weight: 500; min-width: 80px;'>Gênero:</span>
            <span style='color: white;'>{artist_data['gender'].title()}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # País
    st.markdown(f"""
    <div style='display: flex; align-items: center; margin-bottom: 8px;'>
        <span style='color: {COLORS["accent"]}; font-weight: 500; min-width: 80px;'>País:</span>
        <span style='color: white;'>{artist_data['country']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Gêneros
    st.markdown(f"""
    <div style='display: flex; align-items: flex-start;'>
        <span style='color: {COLORS["accent"]}; font-weight: 500; min-width: 80px;'>Gêneros:</span>
        <span style='color: white;'>{artist_data['genres']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    # Métricas do Spotify
    st.markdown(f"""
    <div style='background-color: {COLORS["secondary"]}; padding: 12px; border-radius: 10px; margin-top: 75px; margin-bottom: 10px;'>
        <div style='text-align: center; display: flex; flex-direction: column; align-items: center;'>
            <p style='color: white; margin: 0; font-size: 0.9em; font-weight: 500; line-height: 1.2;'>Popularidade no Spotify</p>
            <div style='display: flex; align-items: center; justify-content: center; margin-top: 4px;'>
                <p style='color: white; margin: 0; margin-right: 5px; font-size: 1.5em; font-weight: 700; line-height: 1;'>{int(artist_data['popularity'])}</p>
                <span style='color: {COLORS["accent"]}; font-size: 0.9em; line-height: 1;'>/ 100</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background-color: {COLORS["secondary"]}; padding: 12px; border-radius: 10px;'>
        <div style='text-align: center; display: flex; flex-direction: column; align-items: center;'>
            <p style='color: white; margin: 0; font-size: 0.9em; font-weight: 500; line-height: 1.2;'>Seguidores no Spotify</p>
            <div style='display: flex; align-items: center; justify-content: center; margin-top: 4px;'>
                <p style='color: white; margin: 0; font-size: 1.5em; font-weight: 700; line-height: 1;'>{int(artist_data['followers']):,}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Seção de Shows
st.write("### Shows")

# Filtra os shows do artista selecionado
artist_past_events = past_events_df[past_events_df['spotify_id'] == st.session_state.selected_artist_id].copy()
artist_future_events = future_events_df[future_events_df['spotify_id'] == st.session_state.selected_artist_id].copy()

# Shows Futuros
if not artist_future_events.empty:
    st.write("#### Próximos Shows")
    # Ordena os shows por data e limita para 5
    artist_future_events['event_date'] = pd.to_datetime(artist_future_events['event_date'])
    artist_future_events = artist_future_events.sort_values('event_date').head(5)

    # Exibe os shows
    for _, show in artist_future_events.iterrows():
        with st.expander(f"{show['venue_name']} - {show['event_date'].strftime('%d/%m/%Y')}"):
            st.write(f"**Local:** {show['venue_name']}")
            st.write(f"**Data:** {show['event_date'].strftime('%d/%m/%Y')}")
            st.write(f"**Cidade:** {show['venue_city']}")
            st.write(f"**País:** {show['venue_country']}")

# Shows Passados
if not artist_past_events.empty:
    st.write("#### Shows Passados")
    # Ordena os shows por data e limita para 5
    artist_past_events['event_date'] = pd.to_datetime(artist_past_events['event_date'])
    artist_past_events = artist_past_events.sort_values('event_date', ascending=False).head(5)

    # Exibe os shows
    for _, show in artist_past_events.iterrows():
        with st.expander(f"{show['venue_name']} - {show['event_date'].strftime('%d/%m/%Y')}"):
            st.write(f"**Local:** {show['venue_name']}")
            st.write(f"**Data:** {show['event_date'].strftime('%d/%m/%Y')}")
            st.write(f"**Cidade:** {show['venue_city']}")
            st.write(f"**País:** {show['venue_country']}")

if artist_future_events.empty and artist_past_events.empty:
    st.info("Não há shows disponíveis para este artista.") 