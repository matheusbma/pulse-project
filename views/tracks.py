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
        return artists_df, tracks_df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        return None, None

# Carrega os dados
artists_df, tracks_df = load_data()

if artists_df is None:
    st.stop()

# Sidebar - Seleção do artista
st.sidebar.markdown("### Procure seu artista favorito")
selected_artist = st.sidebar.selectbox(
    "Artista",
    options=sorted(artists_df['artist_name'].unique()),
    index=sorted(artists_df['artist_name'].unique()).index(st.session_state.get('selected_artist', sorted(artists_df['artist_name'].unique())[0])) if 'selected_artist' in st.session_state else 0,
    key="artist_selector_tracks",
    label_visibility="collapsed"
)

# Atualiza o estado da sessão apenas se o artista selecionado mudou
if selected_artist != st.session_state.get('selected_artist'):
    st.session_state.selected_artist = selected_artist
    st.session_state.selected_artist_id = artists_df[artists_df['artist_name'] == selected_artist]['spotify_id'].iloc[0]
    st.rerun()

# Cabeçalho
artist_data = artists_df[artists_df['artist_name'] == selected_artist].iloc[0]
st.markdown(f"""
    <div style='display: flex; align-items: center; margin-bottom: 2rem;'>
        <h2 style='color: white; margin-bottom: 0;'>{selected_artist}</h2>
        <a href='{artist_data['spotify_url']}' target='_blank' style='margin-left: -20px; text-decoration: none;'>
            <img src='https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg' width='20'>
        </a>
    </div>
""", unsafe_allow_html=True)

# Filtra as músicas do artista selecionado
artist_tracks = tracks_df[tracks_df['spotify_id'] == st.session_state.selected_artist_id].copy()

if not artist_tracks.empty:
    # Ordena as músicas por popularidade
    artist_tracks = artist_tracks.sort_values('popularity', ascending=False)

    # Exibe as músicas
    st.write("### Músicas")
    for _, track in artist_tracks.iterrows():
        with st.expander(f"{track['track_name']}"):
            st.write(f"**Popularidade:** {int(track['popularity'])}/100")
else:
    st.info("Não há músicas disponíveis para este artista.") 