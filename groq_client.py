import os
from groq import Groq

def get_health_prediction(full_name, age, glucose, haemoglobin, cholesterol):
    """
    Calls Groq LLaMA 3.3 70b to generate a health risk assessment
    based on patient biomarker values.
    """
    try:
        import streamlit as st
        api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    except Exception:
        api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        return "⚠️ Groq API key not configured. Add GROQ_API_KEY to .streamlit/secrets.toml or environment variables."

    client = Groq(api_key=api_key)

    prompt = f"""You are a clinical decision support AI assistant. Analyze the following patient biomarker data and provide a brief, professional health risk assessment.

Patient Information:
- Name: {full_name}
- Age: {age} years
- Fasting Glucose: {glucose} mg/dL
- Haemoglobin: {haemoglobin} g/dL
- Total Cholesterol: {cholesterol} mg/dL

Reference Ranges:
- Glucose (fasting): Normal 70–99, Pre-diabetic 100–125, Diabetic ≥126 mg/dL
- Haemoglobin: Normal male 13.5–17.5, female 12.0–15.5 g/dL
- Total Cholesterol: Desirable <200, Borderline 200–239, High ≥240 mg/dL

Provide a concise health assessment in 3–4 sentences covering:
1. Overall risk level (Low / Moderate / High)
2. Key findings based on the biomarker values
3. Recommended next steps or lifestyle advice

Be professional, precise, and avoid alarmist language. Do not diagnose — only assess risk and recommend consultation where appropriate. Do not use markdown formatting in your response."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are MIRA, a Medical Intelligence clinical support assistant. Provide concise, professional health risk assessments based on biomarker data."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI assessment unavailable: {str(e)}"


def calculate_age(dob_str):
    from datetime import date, datetime
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except Exception:
        return "Unknown"
