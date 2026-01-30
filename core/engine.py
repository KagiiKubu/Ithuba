import os
import re
from groq import Groq
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class IthubaEngine:
    def __init__(self):
        # Initialize clients with environment variables
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.llm = genai.GenerativeModel('gemini-1.5-flash')

    def redact_pii(self, text):
        """Simple privacy layer to redact emails and phone numbers."""
        # This shows you care about POPIA/GDPR compliance mentioned in the job post
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b(?:\+27|0)\d{9}\b'
        text = re.sub(email_pattern, "[EMAIL REDACTED]", text)
        text = re.sub(phone_pattern, "[PHONE REDACTED]", text)
        return text

    def generate_professional_profile(self, raw_text):
        """Main agent logic to transform casual speech into professional skills."""
        clean_text = self.redact_pii(raw_text)
        
        system_prompt = f"""
        You are a specialized Career Architect for the South African labor market.
        
        INPUT FROM USER: "{clean_text}"
        
        YOUR TASK:
        1. Extract "Shadow Skills": Identify professional competencies hidden in informal language.
        2. Professional Summary: Write a high-impact summary suitable for a LinkedIn 'About' section.
        3. Key Achievements: List 3-4 bullet points using strong action verbs (e.g., Orchestrated, Managed, Optimized).
        4. "I Am Enough" Affirmation: End with a personalized, empowering message in the style of Marisa Peer.
        
        STRICT FORMAT: Use Markdown with Bold headers. Do not use generic filler text.
        """
        
        response = self.llm.generate_content(system_prompt)
        return response.text
    
    def transcribe_audio(self, audio_file):
        """Uses Groq's Whisper-v3 to turn South African speech into text."""
        try:
            transcription = self.groq_client.audio.transcriptions.create(
                file=(audio_file.name, audio_file.read()),
                model="whisper-large-v3",
                response_format="text"
            )
            return transcription
        except Exception as e:
            return f"Error transcribing audio: {e}"