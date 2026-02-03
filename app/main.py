import streamlit as st
import sys
import os
from audio_recorder_streamlit import audio_recorder

# 1. Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Local imports
from core.utils import create_pdf
from core.engine import IthubaEngine
from core.languages import UI_TRANSLATIONS # New import

# Page Config
st.set_page_config(page_title="Ithuba", page_icon="🇿🇦", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0A1F11 0%, #1B3322 100%); }
    .stButton>button { border-radius: 20px; border: 1px solid #2E7D32; background-color: transparent; color: #E8F5E9; }
    .stButton>button:hover { background-color: #2E7D32; color: white; }
    .stTextArea textarea { background-color: #1B3322 !important; color: #E8F5E9 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Define language first) ---
st.sidebar.title("⚙️ Settings")
language = st.sidebar.selectbox(
    "Interface Language Preference:",
    list(UI_TRANSLATIONS.keys())
)

# Pull the translations for the selected language
t = UI_TRANSLATIONS[language]

st.sidebar.divider()
st.sidebar.title(t["about_head"])
st.sidebar.info(t["mission"])

# Initialize Engine
@st.cache_resource
def get_engine():
    return IthubaEngine()

engine = get_engine()

# --- MAIN UI (Using the 't' dictionary) ---
st.title(t["title"])
st.subheader(t["subtitle"])

st.divider()

# --- Audio Section ---
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""

st.write(f"### {t['step1']}")
col_rec, col_up = st.columns(2)

with col_rec:
    recorded_audio = audio_recorder(text="", icon_size="3x", neutral_color="#2E7D32")

with col_up:
    uploaded_audio = st.file_uploader("", type=["mp3", "wav", "m4a"])

audio_source = recorded_audio if recorded_audio else uploaded_audio

if audio_source:
    with st.spinner("..."):
        try:
            raw_text = engine.transcribe_audio(audio_source)
            st.session_state.transcribed_text = raw_text
        except Exception as e:
            st.error(f"Error: {e}")

# --- Input Section ---
st.write(f"### {t['step2']}")
user_input = st.text_area(
    "",
    value=st.session_state.transcribed_text,
    placeholder=t["placeholder"],
    height=150
)

col1, col2 = st.columns([1, 4])
with col1:
    generate_btn = st.button(t["gen_btn"])

# --- Logic Execution ---
if generate_btn:
    if user_input:
        with st.spinner("Processing..."):
            try:
                # We keep the CV generation in English for professional standard
                profile = engine.generate_professional_profile(user_input, target_language="English")
                
                st.success("Success!")
                st.markdown("---")
                st.markdown(profile)
                
                pdf_data = create_pdf(profile)
                st.download_button(
                    label="Download PDF",
                    data=pdf_data,
                    file_name="Ithuba_Profile.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error: {e}")