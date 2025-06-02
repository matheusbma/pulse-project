import streamlit as st
import pandas as pd
from config import COLORS, apply_custom_css

# Aplica o CSS personalizado
apply_custom_css()

# Carregamento dos dados
@st.cache_data
def load_data():
    try:
        artists_df = pd.read_csv('data/artists.csv')
        related_df = pd.read_csv('data/related_artists.csv')
        
        # Padroniza os nomes dos artistas
        artists_df['artist_name'] = artists_df['artist_name'].apply(lambda x: x.title() if pd.notna(x) else x)
        related_df['related_artist_name'] = related_df['related_artist_name'].apply(lambda x: x.title() if pd.notna(x) else x)
        
        return artists_df, related_df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        return None, None

# Carrega os dados
artists_df, related_df = load_data()

if artists_df is None:
    st.stop()

# Sidebar - Seleção do artista
st.sidebar.markdown("### Procure seu artista favorito")
selected_artist = st.sidebar.selectbox(
    "Artista",
    options=sorted(artists_df['artist_name'].unique()),
    index=sorted(artists_df['artist_name'].unique()).index(st.session_state.get('selected_artist', sorted(artists_df['artist_name'].unique())[0])) if 'selected_artist' in st.session_state else 0,
    key="artist_selector_related",
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

# Artistas relacionados
related_artists = related_df[related_df['spotify_id'] == st.session_state.selected_artist_id].copy()

if not related_artists.empty:
    st.write("### Artistas Relacionados")
    
    # Agrupa os artistas relacionados por similaridade
    for _, related in related_artists.iterrows():
        related_artist_data = artists_df[artists_df['artist_name'] == related['related_artist_name']]
        
        if not related_artist_data.empty:
            related_artist_data = related_artist_data.iloc[0]
            
            with st.expander(f"{related['related_artist_name']}"):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    image_url = related_artist_data['image_url'] if pd.notna(related_artist_data['image_url']) else 'https://via.placeholder.com/200x200?text=No+Image'
                    st.image(image_url, width=200)
                
                with col2:
                    st.write(f"**Tipo:** {related_artist_data['artist_type'].title()}")
                    st.write(f"**País:** {related_artist_data['country']}")
                    st.write(f"**Popularidade:** {int(related_artist_data['popularity'])}/100")
                    st.write(f"**Seguidores:** {int(related_artist_data['followers']):,}")
                    if pd.notna(related_artist_data['genres']):
                        st.write(f"**Gêneros:** {related_artist_data['genres']}")
                    
                    st.markdown(f"[Ver no Spotify]({related_artist_data['spotify_url']})")
else:
    st.info("Não há artistas relacionados disponíveis.") 