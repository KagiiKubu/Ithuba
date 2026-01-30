import streamlit as st
import sys
import os

# This ensures the app can find the 'core' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.engine import IthubaEngine

# Page Config
st.set_page_config(page_title="Ithuba", page_icon="🇿🇦", layout="centered")

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

audio_input = st.file_uploader("Upload a voice note (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])

if audio_input:
    with st.spinner("Transcribing your voice..."):
        # Transcribe the audio
        raw_text = engine.transcribe_audio(audio_input)
        st.info(f"Transcribed: {raw_text}")
        # Set this as the user_input for the next step
        user_input = raw_text


# Input Section
user_input = st.text_area(
    "Describe your daily work/business:",
    placeholder="e.g., 'I run a small catering biz from home, I handle all the cooking, buying stock, and keeping customers happy on WhatsApp.'",
    height=150
)

col1, col2 = st.columns([1, 4])

with col1:
    generate_btn = st.button("Generate ✨")

# Logic Execution
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
                
                # "I Am Enough" Branding
                st.info("💡 Remember: Your lived experience is your greatest asset.")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a description first!")

# Footer
st.sidebar.title("About")
st.sidebar.info("""
Project Ithuba is a Junior AI Engineering showcase project focused on 
socio-economic impact and data privacy.
""")