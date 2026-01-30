# 🇿🇦 Project Ithuba (Opportunity)

**"Your Voice is Your CV"**

Project Ithuba is an AI-powered agentic workflow built to solve a systemic South African challenge: the "Visibility Gap." Millions of talented individuals in the informal economy lack formal CVs. This tool allows them to speak their experience in their own words and uses AI to translate that into a professional, industry-standard digital profile.

---

## 🛠 Tech Stack & Architecture
- **Language:** Python 3.10+
- **LLM Orchestration:** Google Gemini 1.5 Flash (for high-speed skill extraction)
- **Speech-to-Text:** Whisper-large-v3 via Groq (Optimized for SA accents)
- **UI:** Streamlit (Rapid prototyping for internal/client tools)
- **Security:** PII-Redaction layer for POPIA/GDPR compliance


## 🌟 Key Engineering Features
- **Agentic Skill Extraction:** Beyond simple transcription, the system uses an AI agent to identify "Shadow Skills" (e.g., turning "managing community water distribution" into "Logistics & Resource Operations").
- **Privacy-First:** Designed with a focus on sensitive data, ensuring user identity is protected during LLM processing.
- **South African Context:** Prompted specifically to recognize local industry terminology and informal economy nuances.

## 🚀 Impact Goal
Aligned with the "I Am Enough" philosophy, Project Ithuba empowers users by showing them that their existing experience—regardless of formal titles—is valuable and "enough" for the modern workforce.

## 📥 Getting Started
1. **Clone the repo:** `git clone https://github.com/your-username/project-ithuba`
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Set up environment variables:** Create a `.env` file with your `GROQ_API_KEY` and `GEMINI_API_KEY`.
4. **Run the app:** `streamlit run app/main.py`