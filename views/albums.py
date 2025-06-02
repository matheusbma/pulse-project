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

    # Exibe a discografia
    st.write("### Discografia")
    for _, album in artist_albums.iterrows():
        year = album['release_date'] if pd.notna(album['release_date']) else 'N/A'
        with st.expander(f"{album['album_name']} ({year})"):
            st.write(f"**Tipo:** {album['type'].title()}")
            st.write(f"**Ano de Lançamento:** {year}")
            st.write(f"**Total de Faixas:** {album['total_tracks']}")
else:
    st.info("Não há álbuns disponíveis para este artista.") 