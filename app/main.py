import streamlit as st
import sys
import os
from audio_recorder_streamlit import audio_recorder

ISO_LANG_MAP = {
    "English": "en",
    "isiZulu": "zu",
    "isiXhosa": "xh",
    "Afrikaans": "af",
    "Sepedi": "nso",   # Northern Sotho
    "Setswana": "tn",
    "Sesotho": "st",
    "Xitsonga": "ts",
    "siSwati": "ss",
    "Tshivenda": "ve",
    "isiNdebele": "nr"
}

# 1. Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Local imports
from core.utils import create_pdf
from core.engine import IthubaEngine
from core.languages import UI_TRANSLATIONS 

# --- INITIALIZE SESSION STATE ---
if 'pdf_data' not in st.session_state:
    st.session_state.pdf_data = None
if 'current_profile' not in st.session_state:
    st.session_state.current_profile = None
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""

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

# --- SIDEBAR ---
st.sidebar.title("⚙️ Settings")
language = st.sidebar.selectbox("Interface Language Preference:", list(UI_TRANSLATIONS.keys()))
t = UI_TRANSLATIONS[language]

st.sidebar.divider()
st.sidebar.title(t["about_head"])
st.sidebar.info(t["mission"])

# Initialize Engine
@st.cache_resource
def get_engine():
    return IthubaEngine()
engine = get_engine()

# --- MAIN UI ---
st.title(t["title"])
st.subheader(t["subtitle"])
st.divider()

# --- Step 1: Audio Section ---
st.write(f"### {t['step1']}")
col_rec, col_up = st.columns(2)
with col_rec:
    recorded_audio = audio_recorder(text="", icon_size="3x", neutral_color="#2E7D32")
with col_up:
    uploaded_audio = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"], label_visibility="collapsed")

audio_source = recorded_audio if recorded_audio else uploaded_audio
if audio_source:
    with st.spinner("Transcribing..."):
        try:
            # Pass the actual name of the language selected in the sidebar
            st.session_state.transcribed_text = engine.transcribe_audio(
                audio_source, 
                lang_name=language # Pass "isiZulu", "isiXhosa", etc.
            )
        except Exception as e:
            st.error(f"Error transcribing: {e}")

# --- Step 2: Input Section ---
st.write(f"### {t['step2']}")
user_input = st.text_area("Review your story:", value=st.session_state.transcribed_text, height=150)

# --- Step 3: Personalization & Job Context ---
st.write(f"### 👤 {t.get('step3', 'Step 3: Personalize')}")
full_name = st.text_input("Enter your Full Name (for the PDF header):", placeholder="e.g. Sipho Khumalo")

st.write(f"### 🎯 Step 4: Target Job (Optional)")
target_jd = st.text_area("Paste Job Description:", height=100)

generate_btn = st.button(t["gen_btn"])

# --- Logic Execution ---
if generate_btn and user_input:
    with st.spinner("Engineering your professional profile..."):
        try:
            # 1. Generate text via AI
            profile_text = engine.generate_professional_profile(
                user_input, 
                job_description=target_jd
            )
            # 2. Store text in state
            st.session_state.current_profile = profile_text
            
            # 3. Create PDF and pass the user's name
            # If name is empty, we fall back to a generic label
            pdf_bytes = create_pdf(profile_text, user_name=full_name if full_name else "Valued Candidate")
            
            if pdf_bytes:
                st.session_state.pdf_data = pdf_bytes
                st.success("Success! Your ATS-Optimized CV is ready.")
            else:
                st.error("Text was generated, but PDF creation failed.")
                
        except Exception as e:
            st.error(f"Error during generation: {e}")

# --- DISPLAY (Always runs if content exists) ---
if st.session_state.current_profile:
    st.markdown("---")
    st.markdown("### 📄 Preview")
    st.markdown(st.session_state.current_profile)
    
    if st.session_state.pdf_data:
        st.download_button(
            label="📥 Download Professional CV (PDF)",
            data=st.session_state.pdf_data,
            file_name=f"Ithuba_CV_{full_name.replace(' ', '_') if full_name else 'Candidate'}.pdf",
            mime="application/pdf",
            key="final_prod_download"
        )