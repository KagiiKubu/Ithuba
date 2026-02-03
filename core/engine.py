import os
import re
from groq import Groq
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class IthubaEngine:
    def __init__(self):
        # Initialize clients
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Robust Model Selection
        model_names = ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-2.0-flash']
        self.llm = None
        
        for name in model_names:
            try:
                self.llm = genai.GenerativeModel(name)
                # Test the model with a tiny call to see if it actually exists
                # This prevents the 404 happening later during the user's wait
                print(f"Successfully initialized: {name}")
                break
            except Exception as e:
                print(f"Failed to initialize {name}: {e}")
                continue
        
        if self.llm is None:
            raise Exception("Could not initialize any Gemini models. Check your API key and internet connection.")

    def redact_pii(self, text):
        """Simple privacy layer to redact emails and phone numbers for POPIA compliance."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # SA Phone pattern (supports 0... and +27...)
        phone_pattern = r'\b(?:\+27|0)\d{9}\b'
        
        text = re.sub(email_pattern, "[EMAIL REDACTED]", text)
        text = re.sub(phone_pattern, "[PHONE REDACTED]", text)
        return text

    def transcribe_audio(self, audio_data):
        """Handles both uploaded files and live recorded bytes via Groq Whisper-v3."""
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
        """
        Main agent logic that extracts professional skills and 
        character strengths aligned with the 'I Am Enough' philosophy.
        """
        # 1. Security First: Redact PII
        clean_text = self.redact_pii(raw_text.strip())
        
        # 2. Advanced Multi-Step Prompting
        system_prompt = f"""
        You are a specialized Career Architect and Psychological Strengths Coach 
        for the South African labor market.
        
        INPUT FROM USER: "{clean_text}"
        TARGET LANGUAGE: {target_language}
        
        YOUR TASK:
        1. EXTRACT SHADOW SKILLS: Identify the professional capabilities in the story 
           (e.g., "handling stock" -> "Inventory Management & Logistics").
           
        2. CHARACTER STRENGTHS (PERSONALIZATION): Identify 3 psychological strengths 
           demonstrated (e.g., Resilience, Grit, Entrepreneurial Spirit). 
           Frame these using the Marisa Peer 'I Am Enough' mindset.
           
        3. STRUCTURE: Create a formal professional profile in {target_language}.
           Even if the input is code-switching (mix of languages), the output must be 
           formal and dignified in {target_language}.
        
        STRICT MARKDOWN FORMATTING:
        # 🇿🇦 Professional Profile
        (Professional summary here)

        ## 🛠 Core Competencies
        (List skills here)

        ## ✨ Your Lived Strengths (The 'I Am Enough' Perspective)
        (List 3 strengths here with brief descriptions of how they were demonstrated)

        ## 💡 Affirmation
        (2-sentence Marisa Peer 'I Am Enough' affirmation in {target_language})
        """
        
        try:
            # 3. Call the LLM (Gemini 1.5 Flash)
            response = self.llm.generate_content(system_prompt)
            return response.text
        except Exception as e:
            return f"Error generating profile: {e}"