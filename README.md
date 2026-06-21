
# Ava — AI-Powered Desktop Voice Assistant (College Diploma Project)

Ava is an intelligent desktop virtual assistant developed mid 2024. It combines local Natural Language Processing (NLP), Text-to-Speech (TTS), and Speech-to-Text (STT) capabilities with Large Language Model (LLM) processing to provide an interactive, voice-controlled user experience.

*Note: This project represents an early milestone in my software engineering journey. While the codebase is monolithic and serves as a historical academic artifact, it successfully demonstrates end-to-end integration of audio pipelines and generative AI. This project sparked my interest in Data Science and Machine Learning.*

---
<p align="center">
  <img src="your-image-url.png" alt="Centered Image">
</p>

---

## 🗣️ Supported Voice Commands

To interact with the assistant, wait for the voice trigger and use one of the following built-in commands:

### 🤖 After the wake word "Ava":
1. **"розкижи жарт" / "скажи жарт"** — The assistant translates and reads a random programming or general joke.
2. **"відео [video name]"** — Automatically opens YouTube in your default browser and searches for the specified video.
3. **"пошук [query]"** — Opens Google Search in your browser with the requested search term.
4. **"вікіпедія [topic]"** — Parses Wikipedia via its API, extracts a clean text summary in Ukrainian, and reads it out loud.
5. **"кинь монетку" / "монетка"** — Plays a custom coin-flip sound effect (`coin.wav`) and randomly outputs heads or tails ("орел" or "решка").
6. **"запис"** — Enters dictation mode. It records user audio and appends transcribed text line-by-line into a localized `.txt` file until the user says **"стоп"** or **"stop"**.
7. **[Custom Application Name]** — Launches any local desktop application (`.exe`, scripts, etc.) that the user previously added and configured via the "Ваші програми" GUI tab.

### 🧠 After the wake word "GPT":
1. **"[Your open-ended question]"** — The assistant activates the conversational pipeline, routes the prompt directly to the OpenAI API (`GPT-3.5-Turbo`), and utilizes TTS to speak the response back contextually.

---

## 🏗️ Technical Stack

* **Language:** Python
* **GUI Framework:** Tkinter (ttk)
* **Speech-to-Text:** `speech_recognition` (Google Web Speech API with native `uk-UA` support)
* **Text-to-Speech:** `pyttsx3` (Offline multi-voice engine)
* **AI Integration:** OpenAI API (`GPT-3.5-Turbo`)
* **Data Automation:** `json`, `subprocess`, `threading`

---
