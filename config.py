import streamlit as st

# Cores do tema
COLORS = {
    'primary': '#4c0db1',
    'secondary': '#7900ff',
    'accent': '#cb88ff',
    'highlight': '#00c4cc',
    'accent2': '#e43397',
    'text': '#2c3e50',
    'text_light': '#34495e'
}

def setup_page_config():
    """Configuração inicial da página Streamlit."""
    st.set_page_config(
        page_title="Pulse - Dashboard de Artistas",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_custom_css():
    """Aplica o CSS personalizado para o tema."""
    st.markdown(f"""
        <style>
            .main, .stApp, .css-1d391kg {{
                background-color: {COLORS['primary']};
            }}
            /* Ajuste da largura máxima do conteúdo */
            .main .block-container {{
                max-width: 80% !important;
                padding-left: 2rem !important;
                padding-right: 2rem !important;
            }}
            [data-testid="stSidebar"], [data-testid="stSidebar"] > div, [data-testid="stSidebar"] .sidebar-content {{
                background-color: #121640 !important;
                display: flex !important;
                flex-direction: column !important;
            }}
            /* Força a ordem dos elementos no sidebar */
            [data-testid="stSidebar"] > div:first-child {{
                order: -1 !important;
                margin-bottom: 1rem !important;
                padding-bottom: 1rem !important;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
            }}
            [data-testid="stSidebar"] > div:not(:first-child) {{
                order: 1 !important;
            }}
            .stImage > img {{ border-radius: 10px; width: 300px; height: 300px; object-fit: cover; object-position: center; }}
            .stImage > button {{ display: none !important; }}
            h1 {{ color: white; font-size: 2.5rem; font-weight: 700; }}
            h2 {{ color: white; font-size: 1.8rem; font-weight: 600; }}
            h3 {{ color: white; font-size: 1.4rem; font-weight: 500; }}
            p, .stMarkdown {{ color: white; }}
            .stMetric {{
                background-color: {COLORS['secondary']};
                padding: 1rem;
                border-radius: 0.5rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }}
            .stMetric label {{ color: white; font-weight: 600; font-size: 1rem; }}
            .stMetric div {{ color: white; font-size: 1.5rem; font-weight: 700; }}
            .stExpander {{
                background-color: {COLORS['secondary']};
                border-radius: 0.5rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }}
            .stExpander .streamlit-expanderHeader {{ color: white; font-weight: 600; }}
            .stTable {{
                background-color: {COLORS['secondary']};
                border-radius: 0.5rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }}
            .stTable td, .stTable th {{ color: white; }}
            .stInfo {{ background-color: {COLORS['secondary']}; color: white; }}
            .stSidebar, .stSidebar .sidebar-content {{ background-color: #121640 !important; }}
            .stSidebar .sidebar-content .stSelectbox label {{ color: white; }}
            .stSidebar .sidebar-content .stSelectbox div {{ color: white; background-color: {COLORS['secondary']}; }}
            .stSidebar .sidebar-content .stSelectbox div[data-baseweb="select"] {{
                background-color: {COLORS['secondary']} !important;
                border-radius: 0.5rem !important;
                transition: all 0.2s ease-in-out !important;
            }}
            .stSidebar .sidebar-content .stSelectbox div[data-baseweb="select"]:hover {{
                background-color: {COLORS['primary']} !important;
            }}
            .stSidebar .sidebar-content .stSelectbox div[data-baseweb="select"] div {{
                background-color: {COLORS['secondary']} !important;
                color: white !important;
            }}
            .stSidebar .sidebar-content .stSelectbox div[data-baseweb="select"] div:hover {{
                background-color: {COLORS['primary']} !important;
            }}
            a {{ color: {COLORS['accent']}; text-decoration: none; }}
            a:hover {{ color: white; text-decoration: underline; }}
            .stPlotlyChart {{
                background-color: {COLORS['secondary']};
                border-radius: 0.5rem;
                padding: 1rem;
            }}
            /* Override default Streamlit hover colors */
            .stSelectbox div[data-baseweb="select"] div:hover,
            .stSelectbox div[data-baseweb="select"] div[aria-selected="true"],
            .stSelectbox div[data-baseweb="select"] div[aria-selected="true"]:hover,
            .stSelectbox div[data-baseweb="select"] div[role="option"]:hover,
            .stSelectbox div[data-baseweb="select"] div[role="option"][aria-selected="true"],
            .stSelectbox div[data-baseweb="select"] div[role="option"][aria-selected="true"]:hover {{
                background-color: {COLORS['primary']} !important;
            }}
            /* Remove default Streamlit hover effects */
            .stSelectbox:hover, 
            .stExpander:hover,
            .stButton:hover,
            .stRadio:hover,
            .stCheckbox:hover,
            .stSlider:hover,
            .stTextInput:hover,
            .stTextArea:hover,
            .stNumberInput:hover,
            .stDateInput:hover,
            .stTimeInput:hover,
            .stFileUploader:hover {{
                outline: none !important;
                box-shadow: none !important;
            }}
            /* Override any remaining red hover colors */
            [data-baseweb="select"] div:hover,
            [data-baseweb="select"] div[aria-selected="true"],
            [data-baseweb="select"] div[aria-selected="true"]:hover,
            [data-baseweb="select"] div[role="option"]:hover,
            [data-baseweb="select"] div[role="option"][aria-selected="true"],
            [data-baseweb="select"] div[role="option"][aria-selected="true"]:hover {{
                background-color: {COLORS['primary']} !important;
            }}
        </style>
    """, unsafe_allow_html=True) 