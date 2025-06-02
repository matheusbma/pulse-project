import streamlit as st
import pandas as pd
from config import COLORS, apply_custom_css

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
if not future_events.empty:
    st.write("### Próximos Shows")
    future_events = future_events.sort_values('event_date')
    
    for _, event in future_events.iterrows():
        with st.expander(f"{event['event_date'].strftime('%d/%m/%Y')} - {event['venue_name']}"):
            display_event(event)
else:
    st.info("Não há shows futuros agendados.")

# Eventos passados
past_events = past_events_df[past_events_df['spotify_id'] == st.session_state.selected_artist_id].copy()
if not past_events.empty:
    st.write("### Shows Anteriores")
    past_events = past_events.sort_values('event_date', ascending=False)
    
    for _, event in past_events.iterrows():
        with st.expander(f"{event['event_date'].strftime('%d/%m/%Y')} - {event['venue_name']}"):
            display_event(event)
else:
    st.info("Não há shows anteriores registrados.") 