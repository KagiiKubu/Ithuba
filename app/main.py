import streamlit as st
import sys
import os

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
Tell us about your work in your own words, and we'll build your professional profile.
""")

st.divider()

# --- Audio Section ---
audio_input = st.file_uploader("Upload a voice note (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])

# We use a session state variable to keep track of the text across interactions
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""

if audio_input:
    with st.spinner("Transcribing your voice..."):
        # Transcribe only if the file is new
        raw_text = engine.transcribe_audio(audio_input)
        st.session_state.transcribed_text = raw_text
        st.success("Transcription complete!")

# --- Input Section ---
# The value is tied to the session state so audio transcription fills the box
user_input = st.text_area(
    "Describe your daily work/business:",
    value=st.session_state.transcribed_text,
    placeholder="e.g., 'I run a small catering biz from home, I handle all the cooking, buying stock, and keeping customers happy on WhatsApp.'",
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
                
                # --- PDF Generation (Inside the check to avoid NameError) ---
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
        st.warning("Please enter a description or upload audio first!")

# Footer
st.sidebar.title("About")
st.sidebar.info("""
Project Ithuba is a Junior AI Engineering showcase project focused on 
socio-economic impact and data privacy.
""")