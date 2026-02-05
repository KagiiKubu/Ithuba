import streamlit as st
import sys
import os
from audio_recorder_streamlit import audio_recorder

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
# We use a temporary language selection to get the correct 't' dictionary
temp_lang = st.sidebar.selectbox("Select Language / Khetha Ulimi:", list(UI_TRANSLATIONS.keys()))
t = UI_TRANSLATIONS[temp_lang]

st.sidebar.title(t["sidebar_head"])

st.sidebar.divider()
if st.sidebar.button("🗑️ Clear All / Sula Konke"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()
# We re-render the selectbox with the translated label
language = temp_lang # Keep the selection
st.sidebar.write(f"**{t['lang_label']}** {language}")

st.sidebar.divider()
st.sidebar.title(t["about_head"])
st.sidebar.info(t["mission"])

st.sidebar.divider()
st.sidebar.caption("Built for the South African workforce 🇿🇦")
st.sidebar.caption("v1.0.2 | Stable Release")

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
            # Using the 'prompt' method we discussed to avoid 400 errors
            st.session_state.transcribed_text = engine.transcribe_audio(
                audio_source, 
                lang_name=language 
            )
        except Exception as e:
            st.error(f"Error transcribing: {e}")

# --- Step 2: Input Section ---
st.write(f"### {t['step2']}")
user_input = st.text_area(
    t["review_label"], 
    value=st.session_state.transcribed_text, 
    height=150,
    placeholder=t["placeholder_story"]
)

st.write(f"### {t['step3']}")
full_name = st.text_input(t["name_label"], placeholder="e.g. Sipho Khumalo")

# --- Step 4: Target Job ---
st.write(f"### {t['step4']}")
target_jd = st.text_area(
    t["jd_label"], 
    height=100, 
    placeholder=t["placeholder_jd"])

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
            pdf_bytes = create_pdf(profile_text, user_name=full_name if full_name else "Valued Candidate")
            
            if pdf_bytes:
                st.session_state.pdf_data = pdf_bytes
                st.balloons() # This adds a "Wow" factor
                st.success(f"🎊 {t['gen_btn'].replace('✨', '')} Success!")
            else:
                st.error("Text was generated, but PDF creation failed.")
                
        except Exception as e:
            st.error(f"Error during generation: {e}")

# --- DISPLAY (Always runs if content exists) ---
if st.session_state.current_profile:
    st.markdown("---")
    st.markdown(f"### 📄 {t['review_label'].replace(':', '')}")
    st.markdown(st.session_state.current_profile)
    
    if st.session_state.pdf_data:
        st.download_button(
            label="📥 Download Professional CV (PDF)",
            data=st.session_state.pdf_data,
            file_name=f"Ithuba_CV_{full_name.replace(' ', '_') if full_name else 'Candidate'}.pdf",
            mime="application/pdf",
            key="final_prod_download"
        )