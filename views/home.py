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
        return artists_df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        return None

# Carrega os dados
artists_df = load_data()

if artists_df is None:
    st.stop()

# Sidebar - Seleção do artista
st.sidebar.markdown("### Procure seu artista favorito")
selected_artist = st.sidebar.selectbox(
    "Artista",
    options=sorted(artists_df['artist_name'].unique()),
    index=sorted(artists_df['artist_name'].unique()).index(st.session_state.get('selected_artist', sorted(artists_df['artist_name'].unique())[0])) if 'selected_artist' in st.session_state else 0,
    key="artist_selector",
    label_visibility="collapsed"
)

# Atualiza o estado da sessão apenas se o artista selecionado mudou
if selected_artist != st.session_state.get('selected_artist'):
    st.session_state.selected_artist = selected_artist
    st.session_state.selected_artist_id = artists_df[artists_df['artist_name'] == selected_artist]['spotify_id'].iloc[0]
    st.session_state.artists_df = artists_df
    st.rerun()

# Conteúdo principal
st.markdown("""
    <div style='text-align: center; margin-top: 2rem;'>
        <h1 style='color: white; font-size: 3rem; margin-bottom: 1rem;'>Bem-vindo ao <span style='color: #00c4cc;'>Pulse</span></h1>
        <p style='color: white; font-size: 1.2rem; margin-bottom: 2rem;'>
            Sua plataforma completa para explorar o universo musical dos seus artistas favoritos
        </p>
    </div>
""", unsafe_allow_html=True)

# Seção de Introdução
st.markdown("""
    ### Sobre o Pulse
    
    O Pulse é uma plataforma que reúne informações detalhadas sobre artistas musicais, 
    combinando dados de músicas, álbuns, shows e artistas relacionados para oferecer uma experiência completa.
    
    #### O que você pode encontrar aqui:
    
    * 📊 **Geral**: Visão geral do artista, incluindo popularidade, seguidores e gêneros musicais
    * 🎵 **Músicas**: Discografia completa com álbuns e singles
    * 💿 **Álbuns**: Detalhes sobre cada álbum lançado
    * 🎭 **Shows**: Agenda de shows futuros e histórico de apresentações
    * 👥 **Artistas Relacionados**: Descubra artistas similares que você pode gostar
    
    #### Como usar:
    
    1. Selecione um artista no menu lateral
    2. Navegue pelas diferentes páginas usando o menu acima
    3. Explore todas as informações disponíveis sobre seu artista favorito
""")