<div align="center">

<img src="https://img.shields.io/badge/MIRA-Medical%20Intelligence-0a66c2?style=for-the-badge&logo=health&logoColor=white" alt="MIRA"/>

# MIRA — Medical Intelligence Robotic Automation

**AI-powered health prediction platform for clinical biomarker analysis**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-F55036?style=flat-square&logo=groq&logoColor=white)](https://groq.com)
[![SQLite](https://img.shields.io/badge/SQLite-Local%20DB-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-22c55e?style=flat-square)]()

</div>

🔗 **Live Demo:** [mira-health-app.streamlit.app](https://mira-health-app.streamlit.app)

---

## Overview

MIRA is a full-stack health prediction web application that combines **Artificial Intelligence**, **Machine Learning**, and **Predictive Analytics** to assess patient health risk from clinical biomarker data. Built as part of the MIRA — Medical Intelligence Robotic Automation platform, it automates health risk classification and generates AI-powered clinical assessments using Groq's LLaMA 3.3 70B model.

> ⚠️ **Disclaimer:** MIRA is a demonstration application for technical evaluation. It is not a certified medical device and must not be used for clinical diagnosis. Always consult a qualified healthcare professional.

---

## Features

| Feature | Description |
|--------|-------------|
| 🔬 **AI Health Assessment** | LLaMA 3.3 70B via Groq API generates clinical risk assessments from biomarker data |
| 📊 **Risk Classification** | Automatic Low / Moderate / High risk scoring based on standard clinical thresholds |
| 🗄️ **Full CRUD** | Create, Read, Update, Delete patient records with persistent SQLite storage |
| 🔍 **Patient Search** | Live search by name or email across all records |
| ✅ **Input Validation** | Email format, DOB range, and numeric biomarker range validation |
| 📱 **Responsive UI** | Premium dark-theme interface with custom HTML/CSS built on Streamlit |
| 🔒 **Secure** | No API keys committed — environment-based secret management |

---

## Tech Stack

```
┌─────────────────────────────────────────────────┐
│                    MIRA Stack                   │
├──────────────┬──────────────────────────────────┤
│  Frontend    │  Streamlit + Custom HTML/CSS      │
│  Backend     │  Python 3.10+                     │
│  Database    │  SQLite (persistent local storage)│
│  AI Engine   │  Groq API — LLaMA 3.3 70B        │
│  Validation  │  Custom Python utilities          │
└──────────────┴──────────────────────────────────┘
```

---

## Biomarkers Analysed

| Biomarker | Unit | Normal Range | High Risk Threshold |
|-----------|------|-------------|---------------------|
| Fasting Glucose | mg/dL | 70 – 99 | ≥ 126 (Diabetic range) |
| Haemoglobin | g/dL | 12.0 – 17.5 | < 8.0 (Severe anaemia) |
| Total Cholesterol | mg/dL | < 200 | ≥ 240 (High) |

---

## Project Structure

```
MIRA-Medical-Automation/
│
├── app.py              # Main Streamlit application — UI, routing, pages
├── database.py         # SQLite CRUD operations — create, read, update, delete, search
├── groq_client.py      # Groq LLaMA 3.3 70B API integration — health prediction engine
├── utils.py            # Input validation — email, DOB, numeric range checks
├── requirements.txt    # Python dependencies
├── .gitignore          # Excludes secrets, DB files, pycache
└── .streamlit/
    └── secrets.toml    # API key config — NOT committed to GitHub
```

---

## Local Setup

### Prerequisites
- Python 3.10 or above
- A free Groq API key → [console.groq.com](https://console.groq.com)

### 1. Clone the repository
```bash
git clone https://github.com/Rosesharma13/MIRA-Medical-Automation.git
cd MIRA-Medical-Automation
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure your Groq API key

Create the secrets file:
```bash
mkdir .streamlit
```

Add your key inside `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

### 4. Run the app
```bash
streamlit run app.py
```

Open → [http://localhost:8501](http://localhost:8501)

---

## Deployment — Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select this repository → set main file to `app.py`
4. Go to **Settings → Secrets** and add:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```
5. Click **Deploy** — live URL generated instantly

---

## Security

- No API keys or credentials are stored in this repository
- Patient data remains in local SQLite — not transmitted to any external server
- Only anonymised biomarker values (no PII) are sent to Groq for AI analysis
- `.streamlit/secrets.toml` and `*.db` files are excluded via `.gitignore`

---

## Author

**Rose Sharma**
## 👩‍💻 Author
- 🌐 Portfolio: [rosesharma13.github.io](https://rosesharma13.github.io)
- 💼 LinkedIn: [linkedin.com/in/rose-sharma13](https://www.linkedin.com/in/rose-sharma13)
- 📧 Email: rosesharmaa132003@gmail.com

[![GitHub](https://img.shields.io/badge/GitHub-Rosesharma13-181717?style=flat-square&logo=github)](https://github.com/Rosesharma13)

---

<div align="center">
Built with Python · Streamlit · Groq · LLaMA 3.3 70B
</div>
