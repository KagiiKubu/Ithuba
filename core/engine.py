import os
import re
from groq import Groq
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class IthubaEngine:
    def __init__(self):

        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        model_names = ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-2.0-flash']
        self.llm = None
        
        for name in model_names:
            try:
                self.llm = genai.GenerativeModel(name)

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
        phone_pattern = r'\b(?:\+27|0)\d{9}\b'
        
        text = re.sub(email_pattern, "[EMAIL REDACTED]", text)
        text = re.sub(phone_pattern, "[PHONE REDACTED]", text)
        return text

    def transcribe_audio(self, audio_data, lang_name="English"):
        """Handles both uploaded files and live recorded bytes via Groq Whisper-v3."""

        sa_prompt = f"This is a South African person speaking {lang_name} about their professional work experience and skills."
        try:
            if isinstance(audio_data, bytes):
                file_to_send = ("audio.wav", audio_data)
            else:
                file_to_send = (audio_data.name, audio_data.read())

            transcription = self.groq_client.audio.transcriptions.create(
                file=file_to_send,
                model="whisper-large-v3",
                prompt=sa_prompt,
                response_format="text"
            )
            return transcription
        except Exception as e:
            return f"Error transcribing audio: {e}"

    def generate_professional_profile(self, raw_text, target_language="English", job_description=""):
        """
        Generates an ATS-optimized CV. If a job_description is provided,
        it performs a keyword-match to bypass automated filters.
        """
        clean_text = self.redact_pii(raw_text.strip())

        jd_context = f"TARGET JOB DESCRIPTION: {job_description}" if job_description else "No specific job description provided."

        system_prompt = f"""
        You are a Senior Technical Recruiter and ATS (Applicant Tracking System) Expert.
        
        INPUT FROM USER: "{clean_text}"
        {jd_context}
        TARGET LANGUAGE: {target_language}

        CRITICAL INSTRUCTION: 
        - NEVER use placeholders like [Date], [City], or [Company Name]. 
        - If a specific date, location, or company name is NOT mentioned in the user's story, DO NOT include a line for it.
        - Focus on the skills and responsibilities described.
        - Format the output clearly using professional headings.
            
        YOUR TASK:
        1. ATS OPTIMIZATION: Use high-traffic industry keywords found in the target job description. 
           Translate informal experience into professional terminology (e.g., 'selling to people' -> 'Direct Sales & Relationship Management').
           
        2. QUANTIFIABLE RESULTS: Wherever possible, estimate impact (e.g., 'Optimized inventory to reduce waste' or 'Maintained 100% service availability').
           
        3. STRUCTURE: Create an industry-standard CV layout. 
           Even with code-switching, the output must be professional {target_language}.
        
        STRICT MARKDOWN FORMATTING:
        # [FULL NAME - REDACTED]
        
        ## 📝 Professional Summary
        (A high-impact summary focusing on years of experience and top-tier skills.)

        ## 🛠 Technical & Core Competencies
        (A list of skills grouped by 'Operational', 'Management', or 'Technical' categories.)

        ## 📈 Professional Experience & Achievements
        (Bullet points using the 'Action + Context + Result' formula.)

        ## ✨ Leadership & Personal Attributes
        (Identify 3 psychological strengths demonstrated in the story. Frame them using the Marisa Peer mindset.)
        """
        
        try:
            response = self.llm.generate_content(system_prompt)
            return response.text
        except Exception as e:
            return f"Error generating profile: {e}"