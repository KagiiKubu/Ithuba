# 🇿🇦 Project Ithuba (Opportunity)

**"Your Voice is Your CV"**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://ithu-ba.streamlit.app)

Project Ithuba is an AI-powered agentic workflow built to solve a systemic South African challenge: the **"Visibility Gap."** Millions of talented individuals in the informal economy lack formal CVs. This tool allows them to speak their experience in their own words and uses AI to translate that into a professional, industry-standard digital profile.

---

## 🔗 Live Link
**Try the app here:** [ithu-ba.streamlit.app](https://ithu-ba.streamlit.app)

---

## 🛠 Tech Stack & Architecture
- **Language:** Python 3.11+
- **LLM Orchestration:** Google Gemini 2.5 Flash (for high-speed skill extraction)
- **Speech-to-Text:** OpenAI Whisper via Groq (Optimized for SA accents & speed)
- **PDF Generation:** FPDF2 (In-memory byte-stream generation)
- **UI:** Streamlit (Customized with CSS for a premium dark-mode experience)



## 🌟 Key Engineering Features
- **Agentic Skill Extraction:** Beyond simple transcription, the system identifies "Shadow Skills" (e.g., converting "managing community water distribution" into "Logistics & Resource Operations").
- **POPIA Mindful:** Designed with a focus on data privacy, ensuring user experience is handled securely.
- **South African Context:** Prompt-engineered specifically to recognize local industry terminology (e.g., "spaza", "bakkie", "piece-work") and informal economy nuances.
- **Multilingual Support:** UI and processing support for English, isiZulu, and Afrikaans.

## 📁 Project Structure
```text
ithuba/
├── app/
│   └── main.py          # Streamlit UI & Session State Logic
├── core/
│   ├── engine.py        # AI Orchestration (Gemini + Whisper)
│   ├── utils.py         # PDF Generation & Text Processing
│   └── languages.py     # UI Translation Dictionaries
├── requirements.txt     # Optimized Production Dependencies
└── .env                 # Template for API Keys