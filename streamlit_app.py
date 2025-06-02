import streamlit as st
from config import setup_page_config, apply_custom_css
import pandas as pd

# Configuração inicial da página (apenas uma vez)
setup_page_config()
apply_custom_css()

# Inicialização do estado da sessão
if 'selected_artist' not in st.session_state:
    try:
        artists_df = pd.read_csv('data/artists.csv')
        st.session_state.selected_artist = sorted(artists_df['artist_name'].unique())[0]
        st.session_state.selected_artist_id = artists_df[artists_df['artist_name'] == st.session_state.selected_artist]['spotify_id'].iloc[0]
    except Exception as e:
        st.error(f"Erro ao inicializar o estado: {str(e)}")

# Definição das páginas
home_page = st.Page(
    "views/home.py",
    title="Bem-vindo ao Pulse",
    icon="🎧",
    default=True
)

general_page = st.Page(
    "views/general.py",
    title="Geral",
    icon="📊"
)

tracks_page = st.Page(
    "views/tracks.py",
    title="Músicas",
    icon="🎵"
)

albums_page = st.Page(
    "views/albums.py",
    title="Álbuns",
    icon="💿"
)

shows_page = st.Page(
    "views/shows.py",
    title="Shows",
    icon="🎭"
)

related_artists_page = st.Page(
    "views/related_artists.py",
    title="Artistas Relacionados",
    icon="👥"
)

# Configuração da navegação
pg = st.navigation([
    home_page,
    general_page,
    tracks_page,
    albums_page,
    shows_page,
    related_artists_page
])

# Executa a navegação
pg.run() 