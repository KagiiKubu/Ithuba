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
    
    def transcribe_audio(self, audio_data):
        """Handles both uploaded files and live recorded bytes."""
        try:
            # If it's live recording (bytes)
            if isinstance(audio_data, bytes):
                file_to_send = ("audio.wav", audio_data)
            else:
                # If it's an uploaded file object
                file_to_send = (audio_data.name, audio_data.read())

            transcription = self.groq_client.audio.transcriptions.create(
                file=file_to_send,
                model="whisper-large-v3",
                response_format="text"
            )
            return transcription
        except Exception as e:
            return f"Error transcribing audio: {e}"
        

    def generate_professional_profile(self, raw_text, target_language="English"):
        """Main agent logic with multi-language support."""
        clean_text = self.redact_pii(raw_text)
        
        system_prompt = f"""
        You are a specialized Career Architect for the South African labor market.
        
        INPUT FROM USER: "{clean_text}"
        TARGET LANGUAGE: {target_language}
        
        YOUR TASK:
        1. Extract "Shadow Skills" from the input.
        2. Translate and structure the result into a professional profile in {target_language}.
        3. Even if the input is a mix of languages (code-switching), the output must be formal {target_language}.
        4. End with a 2-sentence Marisa Peer 'I Am Enough' affirmation in {target_language}.
        
        STRICT FORMAT: Use Markdown with Bold headers.
        """
        
        response = self.llm.generate_content(system_prompt)
        return response.text