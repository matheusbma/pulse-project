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
        tracks_df = pd.read_csv('data/tracks.csv')  # Voltando para o arquivo original
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

# Filtra as faixas do artista selecionado
artist_tracks = tracks_df[tracks_df['spotify_id'] == st.session_state.selected_artist_id].copy()

if not artist_tracks.empty:
    # Ordena as músicas por popularidade (maior para menor)
    artist_tracks = artist_tracks.sort_values('popularity', ascending=False)
    
    # Layout em duas colunas para métricas
    col1, col2 = st.columns(2)
    
    with col1:
        avg_popularity = artist_tracks['popularity'].mean()
        st.metric("Popularidade Média", f"{avg_popularity:.1f}")
    
    with col2:
        max_popularity = artist_tracks['popularity'].max()
        st.metric("Música Mais Popular", f"{max_popularity}")
    
    # 1. TOP 10 MÚSICAS MAIS POPULARES
    st.write("### 🏆 Top 10 Músicas Mais Populares")
    
    top_10 = artist_tracks.head(10)
    
    # Top 10 músicas mais populares
    fig_bar = px.bar(
        top_10,
        x='popularity',
        y='track_name',
        orientation='h',
        title='Top 10 Músicas Mais Populares',
        labels={'popularity': 'Popularidade', 'track_name': 'Música'},
        color='popularity',
        color_continuous_scale=[[0, COLORS['accent2']], [0.5, COLORS['accent']], [1, COLORS['highlight']]],
        height=450
    )
    
    # Personalizar o layout
    fig_bar.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        showlegend=False
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # 2. DISTRIBUIÇÃO DE POPULARIDADE
    st.write("### 📊 Distribuição de Popularidade")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histograma de popularidade
        fig_hist = px.histogram(
            artist_tracks,
            x='popularity',
            nbins=20,
            title='Distribuição de Popularidade das Músicas',
            labels={'popularity': 'Popularidade', 'count': 'Número de Músicas'},
            color_discrete_sequence=['#00a8b5'],
            height=400,
            width=500
        )
        fig_hist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis=dict(
                title='Popularidade (0 = Menos Popular | 100 = Mais Popular)',
                tickmode='linear',
                tick0=0,
                dtick=10,
                tickvals=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                ticktext=['0\n(Baixa)', '10', '20', '30\n(Média)', '40', '50', '60', '70\n(Alta)', '80', '90', '100\n(Máxima)'],
                gridcolor='rgba(255,255,255,0.1)',
                color='white',
                range=[-5, 105]
            ),
            yaxis=dict(
                title='Número de Músicas',
                gridcolor='rgba(255,255,255,0.1)',
                color='white'
            )
        )
        
        # Adicionar linhas de referência para faixas importantes
        fig_hist.add_vline(x=30, line_dash="dash", line_color="rgba(255,255,255,0.3)", 
                          annotation_text="Popularidade Média", annotation_position="top")
        fig_hist.add_vline(x=70, line_dash="dash", line_color="rgba(255,255,255,0.3)", 
                          annotation_text="Alta Popularidade", annotation_position="top")
        
        st.plotly_chart(fig_hist, use_container_width=False)
    
    with col2:
        # Box plot para análise estatística
        fig_box = px.box(
            artist_tracks,
            y='popularity',
            title='Análise Estatística da Popularidade',
            labels={'popularity': 'Popularidade'},
            color_discrete_sequence=['#a02570'],
            height=400,
            width=500
        )
        fig_box.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=False
        )
        st.plotly_chart(fig_box, use_container_width=False)
    
    # 3. ANÁLISE POR CATEGORIAS DE POPULARIDADE
    st.write("### 🎯 Análise por Categorias")
    
    # Criar categorias baseadas na popularidade
    def categorize_popularity(pop):
        if pop >= 70:
            return "Muito Popular (70+)"
        elif pop >= 50:
            return "Popular (50-69)"
        elif pop >= 30:
            return "Moderado (30-49)"
        else:
            return "Baixa (0-29)"
    
    artist_tracks['categoria'] = artist_tracks['popularity'].apply(categorize_popularity)
    category_counts = artist_tracks['categoria'].value_counts()
    
    # Gráfico de barras das categorias
    fig_categories = px.bar(
        x=category_counts.values,
        y=category_counts.index,
        orientation='h',
        title='Distribuição por Categoria de Popularidade',
        labels={'x': 'Número de Músicas', 'y': 'Categoria'},
        color=category_counts.values,
        color_continuous_scale=[[0, COLORS['accent2']], [0.5, COLORS['accent']], [1, COLORS['highlight']]],
        height=450
    )
    fig_categories.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        showlegend=False,
        title_font_color='white',
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            color='white'
        ),
        yaxis=dict(
            categoryorder='total ascending',
            gridcolor='rgba(255,255,255,0.1)',
            color='white'
        )
    )
    fig_categories.update_traces(
        marker_line_color='rgba(255,255,255,0.2)',
        marker_line_width=1
    )
    st.plotly_chart(fig_categories, use_container_width=True)
    
else:
    st.info("Não há músicas disponíveis para este artista.") 