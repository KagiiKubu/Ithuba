import streamlit as st
import sys
import os
from audio_recorder_streamlit import audio_recorder

# 1. Path setup MUST come before local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Local imports
from core.utils import create_pdf
from core.engine import IthubaEngine

# Page Config
st.set_page_config(page_title="Ithuba", page_icon="🇿🇦", layout="centered")

# Custom CSS for a "Premium Wellness" feel
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0A1F11 0%, #1B3322 100%);
    }
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #2E7D32;
        background-color: transparent;
        color: #E8F5E9;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #2E7D32;
        color: white;
    }
    /* Style for text area to match theme */
    .stTextArea textarea {
        background-color: #1B3322 !important;
        color: #E8F5E9 !important;
    }
    /* Center the audio recorder */
    .stCamera {
        display: flex;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize the AI Engine
@st.cache_resource
def get_engine():
    return IthubaEngine()

engine = get_engine()

# UI Header
st.title("🇿🇦 Project Ithuba")
st.subheader("Your Voice is Your CV")
st.write("""
This tool uses AI to bridge the 'Visibility Gap' in South Africa. 
Record your story or upload a voice note, and we'll build your professional profile.
""")

st.divider()

# --- Audio Section ---
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""

st.write("### 🎙️ Step 1: Provide your story")
col_rec, col_up = st.columns(2)

with col_rec:
    st.write("Record live:")
    # The recorder returns bytes
    recorded_audio = audio_recorder(
        text="Click to record",
        recording_color="#e85c5c",
        neutral_color="#2E7D32",
        icon_size="3x",
    )

with col_up:
    uploaded_audio = st.file_uploader("Or upload a file:", type=["mp3", "wav", "m4a"])

# Process whichever input is provided
audio_source = recorded_audio if recorded_audio else uploaded_audio

if audio_source:
    with st.spinner("AI is listening and transcribing..."):
        try:
            raw_text = engine.transcribe_audio(audio_source)
            st.session_state.transcribed_text = raw_text
            st.success("Voice processed successfully!")
        except Exception as e:
            st.error(f"Transcription error: {e}")

# --- Input Section ---
st.write("### 📝 Step 2: Review or Edit")
user_input = st.text_area(
    "Your work description (extracted from audio or typed):",
    value=st.session_state.transcribed_text,
    placeholder="e.g., 'I manage a small poultry farm, handling feed, sales, and community distribution.'",
    height=150
)

col1, col2 = st.columns([1, 4])

with col1:
    generate_btn = st.button("Generate ✨")

# --- Logic Execution ---
if generate_btn:
    if user_input:
        with st.spinner("Analyzing skills and building your profile..."):
            try:
                # Call the engine logic
                profile = engine.generate_professional_profile(user_input)
                
                # Display Result
                st.success("Professional Profile Generated!")
                st.markdown("---")
                st.markdown(profile)
                
                # --- PDF Generation ---
                pdf_data = create_pdf(profile)
                st.download_button(
                    label="Download your Profile (PDF) 📄",
                    data=pdf_data,
                    file_name="Ithuba_Professional_Profile.pdf",
                    mime="application/pdf"
                )
                
                # "I Am Enough" Branding
                st.info("💡 Remember: Your lived experience is your greatest asset.")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please record your voice or enter a description first!")

# Footer
st.sidebar.title("About")
st.sidebar.info("""
Project Ithuba is a Junior AI Engineering showcase project focused on 
socio-economic impact and data privacy.

**Mission:** Bridging the gap between informal experience and formal recognition.
""")