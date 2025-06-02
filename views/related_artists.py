import streamlit as st
import pandas as pd
from config import COLORS, apply_custom_css
import plotly.express as px

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

    # Filtra os artistas relacionados ao artista selecionado
    related_artists_data = related_df[related_df['spotify_id'] == st.session_state.selected_artist_id].copy()

    if not related_artists_data.empty:
        # Layout em duas colunas para métricas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_related = len(related_artists_data)
            st.metric("Artistas Relacionados", total_related)
        
        with col2:
            avg_popularity = related_artists_data['related_artist_popularity'].mean()
            st.metric("Popularidade Média", f"{avg_popularity:.1f}")
        
        with col3:
            unique_genres = related_artists_data['related_artist_genres'].str.split(', ').explode().nunique()
            st.metric("Gêneros Únicos", unique_genres)

        # 1. COMPARAÇÃO DE POPULARIDADE
        st.write("### 🏆 Comparação de Popularidade")
        
        # Obter dados do artista principal
        main_artist_data = artists_df[artists_df['spotify_id'] == st.session_state.selected_artist_id].iloc[0]
        
        # Top 15 artistas relacionados por popularidade
        top_related = related_artists_data.nlargest(15, 'related_artist_popularity')
        
        # Adicionar o artista principal para comparação
        comparison_data = []
        comparison_data.append({
            'artist_name': f"{main_artist_data['artist_name']} (Principal)",
            'popularity': main_artist_data['popularity']
        })
        
        for _, artist in top_related.iterrows():
            comparison_data.append({
                'artist_name': artist['related_artist_name'],
                'popularity': artist['related_artist_popularity']
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Gráfico de barras comparativo
        fig_comparison = px.bar(
            comparison_df,
            x='popularity',
            y='artist_name',
            orientation='h',
            title=f'Comparação de Popularidade: {selected_artist} vs Artistas Relacionados',
            labels={'popularity': 'Popularidade', 'artist_name': 'Artista'},
            color='popularity',
            color_continuous_scale='RdYlBu_r',
            height=600
        )
        fig_comparison.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=False
        )
        st.plotly_chart(fig_comparison, use_container_width=True)

        # 2. ANÁLISE DE GÊNEROS MUSICAIS
        st.write("### 🎵 Análise de Gêneros Musicais")
        
        # Extrair e contar gêneros
        all_genres = []
        for genres_str in related_artists_data['related_artist_genres'].dropna():
            if genres_str and genres_str != '':
                genres_list = [genre.strip() for genre in genres_str.split(',')]
                all_genres.extend(genres_list)
        
        if all_genres:
            genre_counts = pd.Series(all_genres).value_counts().head(15)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top gêneros - gráfico de barras
                fig_genres = px.bar(
                    x=genre_counts.values,
                    y=genre_counts.index,
                    orientation='h',
                    title='Top 15 Gêneros Musicais',
                    labels={'x': 'Frequência', 'y': 'Gênero'},
                    color=genre_counts.values,
                    color_continuous_scale='Viridis'
                )
                fig_genres.update_layout(
                    yaxis={'categoryorder': 'total ascending'},
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    showlegend=False
                )
                st.plotly_chart(fig_genres, use_container_width=True)
            
            with col2:
                # Nuvem de gêneros - gráfico de pizza dos top 10
                top_10_genres = genre_counts.head(10)
                fig_pie_genres = px.pie(
                    values=top_10_genres.values,
                    names=top_10_genres.index,
                    title='Distribuição dos Top 10 Gêneros',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie_genres.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig_pie_genres, use_container_width=True)

        # 3. DISTRIBUIÇÃO DE POPULARIDADE DOS ARTISTAS RELACIONADOS
        st.write("### 📊 Distribuição de Popularidade")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histograma de popularidade
            fig_hist = px.histogram(
                related_artists_data,
                x='related_artist_popularity',
                nbins=15,
                title='Distribuição de Popularidade dos Artistas Relacionados',
                labels={'related_artist_popularity': 'Popularidade', 'count': 'Número de Artistas'},
                color_discrete_sequence=['#ff6b6b']
            )
            fig_hist.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Box plot estatístico
            fig_box = px.box(
                related_artists_data,
                y='related_artist_popularity',
                title='Análise Estatística da Popularidade',
                labels={'related_artist_popularity': 'Popularidade'},
                color_discrete_sequence=['#4dabf7']
            )
            fig_box.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                showlegend=False
            )
            st.plotly_chart(fig_box, use_container_width=True)

        # 4. ANÁLISE DE CATEGORIAS DE POPULARIDADE
        st.write("### 🎯 Categorias de Popularidade")
        
        # Categorizar artistas por popularidade
        def categorize_popularity(pop):
            if pop >= 60:
                return "Muito Popular (60+)"
            elif pop >= 40:
                return "Popular (40-59)"
            elif pop >= 20:
                return "Moderado (20-39)"
            else:
                return "Emergente (0-19)"
        
        related_artists_data['categoria'] = related_artists_data['related_artist_popularity'].apply(categorize_popularity)
        category_counts = related_artists_data['categoria'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de pizza por categoria
            fig_categories = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title='Distribuição por Categoria de Popularidade',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_categories.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_categories, use_container_width=True)
        
        with col2:
            # Scatter plot: relacionar gêneros com popularidade
            # Pegar um gênero principal para cada artista
            related_artists_data['main_genre'] = related_artists_data['related_artist_genres'].str.split(',').str[0]
            genre_popularity = related_artists_data.groupby('main_genre')['related_artist_popularity'].agg(['mean', 'count']).reset_index()
            genre_popularity = genre_popularity[genre_popularity['count'] >= 2]  # Apenas gêneros com 2+ artistas
            
            if not genre_popularity.empty:
                fig_genre_pop = px.scatter(
                    genre_popularity,
                    x='count',
                    y='mean',
                    size='count',
                    hover_data=['main_genre'],
                    title='Popularidade Média por Gênero (min. 2 artistas)',
                    labels={'count': 'Número de Artistas', 'mean': 'Popularidade Média'},
                    color='mean',
                    color_continuous_scale='Viridis'
                )
                fig_genre_pop.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig_genre_pop, use_container_width=True)

        # 5. NETWORK SIMPLIFICADO - TOP CONEXÕES
        st.write("### 🕸️ Rede de Conexões Musicais")
        
        # Criar uma visualização de rede simplificada
        top_20_related = related_artists_data.nlargest(20, 'related_artist_popularity')
        
        # Criar dados para sunburst (hierarquia de gêneros)
        sunburst_data = []
        
        for _, artist in top_20_related.iterrows():
            genres = artist['related_artist_genres']
            if pd.notna(genres) and genres != '':
                main_genre = genres.split(',')[0].strip()
                sunburst_data.append({
                    'ids': artist['related_artist_name'],
                    'labels': artist['related_artist_name'],
                    'parents': main_genre,
                    'values': artist['related_artist_popularity']
                })
                sunburst_data.append({
                    'ids': main_genre,
                    'labels': main_genre,
                    'parents': selected_artist,
                    'values': 0
                })
        
        # Adicionar artista principal
        sunburst_data.append({
            'ids': selected_artist,
            'labels': selected_artist,
            'parents': '',
            'values': 0
        })
        
        if sunburst_data:
            sunburst_df = pd.DataFrame(sunburst_data).drop_duplicates(subset=['ids'])
            
            fig_sunburst = px.sunburst(
                sunburst_df,
                ids='ids',
                labels='labels',
                parents='parents',
                values='values',
                title=f'Rede de Artistas Relacionados a {selected_artist}',
                color='values',
                color_continuous_scale='Viridis'
            )
            fig_sunburst.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_sunburst, use_container_width=True)

        # 6. TABELA COMPLETA DE ARTISTAS RELACIONADOS
        st.write("### 📋 Lista Completa de Artistas Relacionados")
        
        # Criar tabela organizada
        artists_table = related_artists_data[['related_artist_name', 'related_artist_popularity', 'related_artist_genres']].copy()
        artists_table = artists_table.sort_values('related_artist_popularity', ascending=False)
        artists_table = artists_table.rename(columns={
            'related_artist_name': 'Artista',
            'related_artist_popularity': 'Popularidade',
            'related_artist_genres': 'Gêneros'
        })
        
        st.dataframe(
            artists_table,
            use_container_width=True,
            height=400
        )

else:
    st.info("Não há artistas relacionados disponíveis para este artista.") 