# MIRA – Medical Intelligence Robotic Automation

A full-stack health prediction web application built with Python, Streamlit, SQLite, and Groq's LLaMA 3.3 70B model.

## Features

- **CRUD Operations** — Create, Read, Update, Delete patient records
- **AI Health Assessment** — Groq + LLaMA 3.3 70B generates risk assessments from biomarker data
- **Risk Classification** — Automatic Low / Moderate / High risk scoring
- **Input Validation** — Email format, date of birth, numeric range checks
- **Persistent Storage** — SQLite database
- **Search** — Search patients by name or email
- **Premium UI** — Custom dark-theme interface built on Streamlit

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit + Custom HTML/CSS |
| Backend | Python 3.10+ |
| Database | SQLite |
| AI/ML API | Groq — LLaMA 3.3 70B Versatile |

## Biomarkers Tracked

| Biomarker | Unit | Normal Range |
|-----------|------|-------------|
| Fasting Glucose | mg/dL | 70–99 |
| Haemoglobin | g/dL | 12.0–17.5 |
| Total Cholesterol | mg/dL | < 200 |

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/MIRA-Health-App.git
cd MIRA-Health-App
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Groq API key

**Option A — Local development:**
Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

**Option B — Environment variable:**
```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

Get a free API key at [console.groq.com](https://console.groq.com)

### 4. Run the application
```bash
streamlit run app.py
```

## Project Structure

```
MIRA-Health-App/
├── app.py              # Main Streamlit application + UI
├── database.py         # SQLite CRUD operations
├── groq_client.py      # Groq LLaMA API integration
├── utils.py            # Input validation
├── requirements.txt    # Python dependencies
├── .gitignore
└── .streamlit/
    └── secrets.toml.example
```

## Deployment (Streamlit Cloud)

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Add `GROQ_API_KEY` under **Settings → Secrets**
5. Deploy

## Security Notes

- No API keys or passwords are committed to this repository
- Patient data is stored locally in SQLite — not transmitted externally
- AI assessment uses biomarker values only — no personally identifiable data is sent to Groq

## Disclaimer

MIRA is a demonstration application for technical evaluation purposes. It is not a certified medical device and should not be used for clinical diagnosis. Always consult a qualified healthcare professional.
