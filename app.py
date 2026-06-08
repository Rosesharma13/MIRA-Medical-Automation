import streamlit as st
import pandas as pd
from datetime import date, datetime
from database import init_db, create_patient, read_all_patients, read_patient_by_id, update_patient, delete_patient, search_patients
from groq_client import get_health_prediction, calculate_age
from utils import validate_patient_form

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MIRA – Medical Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Init DB ──────────────────────────────────────────────────────────────────
init_db()

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Base reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0e1a !important;
    color: #e2e8f0;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 2rem 2rem !important; max-width: 1400px !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0d1221 !important;
    border-right: 1px solid #1e2d4a;
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem !important; }

/* ── Sidebar radio buttons ── */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 0.25rem;
    flex-direction: column;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 0.6rem 1rem !important;
    font-size: 0.875rem;
    color: #94a3b8;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #1e2d4a;
    color: #e2e8f0;
    border-color: #2d4a6e;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [data-checked="true"] + label,
[data-testid="stSidebar"] [data-testid="stRadio"] input:checked + div label {
    background: linear-gradient(135deg, #1a3a5c, #0f2a45);
    color: #60a5fa;
    border-color: #2563eb;
}

/* ── Metric cards ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: #0d1221;
    border: 1px solid #1e2d4a;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}
.metric-card.blue::before { background: linear-gradient(90deg, #2563eb, #60a5fa); }
.metric-card.green::before { background: linear-gradient(90deg, #059669, #34d399); }
.metric-card.amber::before { background: linear-gradient(90deg, #d97706, #fbbf24); }
.metric-card.red::before { background: linear-gradient(90deg, #dc2626, #f87171); }
.metric-label { font-size: 0.75rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.08em; color: #64748b; margin-bottom: 0.5rem; }
.metric-value { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: #f1f5f9; }
.metric-sub { font-size: 0.75rem; color: #475569; margin-top: 0.25rem; }

/* ── Section header ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #1e2d4a;
}
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: #f1f5f9;
    margin: 0;
}
.section-badge {
    background: #1e2d4a;
    color: #60a5fa;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.25rem 0.65rem;
    border-radius: 20px;
    border: 1px solid #2d4a6e;
}

/* ── Form container ── */
.form-container {
    background: #0d1221;
    border: 1px solid #1e2d4a;
    border-radius: 16px;
    padding: 2rem;
}
.form-section-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #475569;
    margin-bottom: 0.75rem;
    margin-top: 1.25rem;
}

/* ── Streamlit inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stTextArea"] textarea {
    background: #111827 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.875rem !important;
    padding: 0.6rem 0.85rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stDateInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
    outline: none !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stDateInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
    margin-bottom: 0.3rem !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: #111827 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* ── Buttons ── */
[data-testid="stButton"] > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.5rem !important;
    font-size: 0.875rem !important;
    transition: all 0.2s ease !important;
    border: none !important;
}
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: white !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4) !important;
}
[data-testid="stButton"] > button[kind="secondary"] {
    background: #1e2d4a !important;
    color: #94a3b8 !important;
    border: 1px solid #2d4a6e !important;
}
[data-testid="stButton"] > button[kind="secondary"]:hover {
    background: #2d3f5e !important;
    color: #e2e8f0 !important;
}

/* ── Patient table cards ── */
.patient-card {
    background: #0d1221;
    border: 1px solid #1e2d4a;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.2s ease, transform 0.2s ease;
    cursor: pointer;
}
.patient-card:hover {
    border-color: #2563eb;
    transform: translateX(3px);
}
.patient-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 0.25rem;
}
.patient-email { font-size: 0.8rem; color: #64748b; }
.patient-meta {
    display: flex;
    gap: 1rem;
    margin-top: 0.75rem;
    flex-wrap: wrap;
}
.biomarker-pill {
    background: #111827;
    border: 1px solid #1e2d4a;
    border-radius: 20px;
    padding: 0.2rem 0.65rem;
    font-size: 0.72rem;
    color: #94a3b8;
    font-weight: 500;
}
.biomarker-pill span { color: #60a5fa; font-weight: 600; }
.risk-badge {
    padding: 0.2rem 0.65rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.risk-low { background: #052e16; color: #4ade80; border: 1px solid #166534; }
.risk-moderate { background: #451a03; color: #fbbf24; border: 1px solid #92400e; }
.risk-high { background: #450a0a; color: #f87171; border: 1px solid #991b1b; }

/* ── Remarks box ── */
.remarks-box {
    background: #060d1a;
    border: 1px solid #1e2d4a;
    border-left: 3px solid #2563eb;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.25rem;
    margin-top: 0.75rem;
    font-size: 0.85rem;
    color: #94a3b8;
    line-height: 1.6;
}

/* ── Alert messages ── */
.alert-success {
    background: #052e16;
    border: 1px solid #166534;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    color: #4ade80;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.alert-error {
    background: #450a0a;
    border: 1px solid #991b1b;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    color: #f87171;
    font-size: 0.85rem;
}
.alert-info {
    background: #0c1a36;
    border: 1px solid #1e3a6e;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    color: #60a5fa;
    font-size: 0.85rem;
}

/* ── Loading spinner ── */
.ai-loading {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    color: #60a5fa;
    font-size: 0.875rem;
}
.spinner {
    width: 18px;
    height: 18px;
    border: 2px solid #1e2d4a;
    border-top-color: #2563eb;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Top header ── */
.app-header {
    padding: 1.75rem 0 1.25rem 0;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #1e2d4a;
}
.app-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -0.02em;
}
.app-logo span { color: #2563eb; }
.app-tagline { font-size: 0.8rem; color: #475569; margin-top: 0.15rem; }

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid #1e2d4a;
    margin: 1.5rem 0;
}

/* ── Dataframe override ── */
[data-testid="stDataFrame"] {
    border: 1px solid #1e2d4a !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Session state init ───────────────────────────────────────────────────────
if "edit_patient_id" not in st.session_state:
    st.session_state.edit_patient_id = None
if "view_patient_id" not in st.session_state:
    st.session_state.view_patient_id = None
if "confirm_delete_id" not in st.session_state:
    st.session_state.confirm_delete_id = None

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 1.5rem 0;">
        <div style="font-family:'Space Grotesk',sans-serif; font-size:1.5rem; font-weight:700; color:#f1f5f9;">
            M<span style="color:#2563eb">I</span>RA
        </div>
        <div style="font-size:0.65rem; color:#475569; text-transform:uppercase; letter-spacing:0.15em; margin-top:0.15rem;">
            Medical Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.65rem; font-weight:600; text-transform:uppercase; letter-spacing:0.12em; color:#475569; margin-bottom:0.5rem; padding-left:0.5rem;">Navigation</div>', unsafe_allow_html=True)

    page = st.radio(
        "nav",
        ["🏠  Dashboard", "➕  Add Patient", "📋  All Patients", "🔍  Search"],
        label_visibility="collapsed"
    )

    st.markdown('<hr style="border:none;border-top:1px solid #1e2d4a;margin:1.5rem 0;">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.7rem; color:#475569; line-height:1.6; padding: 0 0.5rem;">
        <div style="color:#60a5fa; font-weight:600; margin-bottom:0.4rem;">AI Engine</div>
        LLaMA 3.3 70B via Groq<br>
        <div style="margin-top:0.5rem; color:#60a5fa; font-weight:600;">Storage</div>
        SQLite · Local Persistent<br>
        <div style="margin-top:0.5rem; color:#60a5fa; font-weight:600;">Framework</div>
        Python · Streamlit
    </div>
    """, unsafe_allow_html=True)

# ─── Main content ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="app-logo">MIRA <span>Health</span></div>
    <div class="app-tagline">Medical Intelligence Robotic Automation — Predictive Health Analytics Platform</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠  Dashboard":
    all_patients = read_all_patients()
    total = len(all_patients)

    # Risk classification helper
    def get_risk_level(p):
        if p["glucose"] >= 126 or p["cholesterol"] >= 240 or p["haemoglobin"] < 8:
            return "High"
        elif p["glucose"] >= 100 or p["cholesterol"] >= 200 or p["haemoglobin"] < 12:
            return "Moderate"
        return "Low"

    high_risk = sum(1 for p in all_patients if get_risk_level(p) == "High")
    moderate_risk = sum(1 for p in all_patients if get_risk_level(p) == "Moderate")
    low_risk = sum(1 for p in all_patients if get_risk_level(p) == "Low")

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card blue">
            <div class="metric-label">Total Patients</div>
            <div class="metric-value">{total}</div>
            <div class="metric-sub">All records in system</div>
        </div>
        <div class="metric-card green">
            <div class="metric-label">Low Risk</div>
            <div class="metric-value">{low_risk}</div>
            <div class="metric-sub">Normal biomarker range</div>
        </div>
        <div class="metric-card amber">
            <div class="metric-label">Moderate Risk</div>
            <div class="metric-value">{moderate_risk}</div>
            <div class="metric-sub">Borderline values</div>
        </div>
        <div class="metric-card red">
            <div class="metric-label">High Risk</div>
            <div class="metric-value">{high_risk}</div>
            <div class="metric-sub">Requires attention</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Recent patients ──
    st.markdown("""
    <div class="section-header">
        <div class="section-title">Recent Patients</div>
        <div class="section-badge">Latest 5</div>
    </div>
    """, unsafe_allow_html=True)

    if not all_patients:
        st.markdown('<div class="alert-info">ℹ️ No patient records yet. Add your first patient from the sidebar.</div>', unsafe_allow_html=True)
    else:
        for p in all_patients[:5]:
            risk = get_risk_level(p)
            risk_class = {"Low": "risk-low", "Moderate": "risk-moderate", "High": "risk-high"}[risk]
            age = calculate_age(p["date_of_birth"])
            st.markdown(f"""
            <div class="patient-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div>
                        <div class="patient-name">{p['full_name']}</div>
                        <div class="patient-email">{p['email']} · Age {age}</div>
                    </div>
                    <span class="risk-badge {risk_class}">{risk} Risk</span>
                </div>
                <div class="patient-meta">
                    <span class="biomarker-pill">Glucose <span>{p['glucose']} mg/dL</span></span>
                    <span class="biomarker-pill">Haemoglobin <span>{p['haemoglobin']} g/dL</span></span>
                    <span class="biomarker-pill">Cholesterol <span>{p['cholesterol']} mg/dL</span></span>
                </div>
                {"<div class='remarks-box'>" + p['remarks'][:200] + ("..." if len(p.get('remarks','')) > 200 else "") + "</div>" if p.get('remarks') else ""}
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ADD PATIENT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "➕  Add Patient":
    st.markdown("""
    <div class="section-header">
        <div class="section-title">Add New Patient</div>
        <div class="section-badge">New Record</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("add_patient_form", clear_on_submit=True):
        st.markdown('<div class="form-section-label">Patient Information</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name", placeholder="e.g. Ananya Sharma")
        with col2:
            email = st.text_input("Email Address", placeholder="e.g. ananya@email.com")

        col3, col4 = st.columns(2)
        with col3:
            dob = st.date_input(
                "Date of Birth",
                min_value=date(1900, 1, 1),
                max_value=date.today(),
                value=date(1990, 1, 1)
            )
        with col4:
            st.markdown('<div style="padding-top:1.8rem; font-size:0.8rem; color:#64748b;">Age will be calculated automatically from DOB.</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-section-label">Biomarker Values</div>', unsafe_allow_html=True)
        col5, col6, col7 = st.columns(3)
        with col5:
            glucose = st.number_input("Fasting Glucose (mg/dL)", min_value=0.0, max_value=600.0, value=90.0, step=0.1, format="%.1f")
        with col6:
            haemoglobin = st.number_input("Haemoglobin (g/dL)", min_value=0.0, max_value=25.0, value=13.5, step=0.1, format="%.1f")
        with col7:
            cholesterol = st.number_input("Total Cholesterol (mg/dL)", min_value=0.0, max_value=700.0, value=180.0, step=0.1, format="%.1f")

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        submitted = st.form_submit_button("🔬 Analyse & Save Patient", use_container_width=True, type="primary")

    if submitted:
        errors = validate_patient_form(full_name, dob, email, glucose, haemoglobin, cholesterol)
        if errors:
            for err in errors:
                st.markdown(f'<div class="alert-error">⚠️ {err}</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Running AI health analysis via MIRA..."):
                age = calculate_age(str(dob))
                remarks = get_health_prediction(full_name, age, glucose, haemoglobin, cholesterol)

            success, msg = create_patient(full_name, str(dob), email, glucose, haemoglobin, cholesterol, remarks)
            if success:
                st.markdown(f'<div class="alert-success">✓ Patient record created and AI analysis completed.</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div style="margin-top:1rem;">
                    <div style="font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.1em; color:#475569; margin-bottom:0.5rem;">AI Health Assessment</div>
                    <div class="remarks-box">{remarks}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-error">⚠️ {msg}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ALL PATIENTS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📋  All Patients":
    all_patients = read_all_patients()

    st.markdown(f"""
    <div class="section-header">
        <div class="section-title">Patient Records</div>
        <div class="section-badge">{len(all_patients)} total</div>
    </div>
    """, unsafe_allow_html=True)

    if not all_patients:
        st.markdown('<div class="alert-info">ℹ️ No patient records found. Add patients from the sidebar.</div>', unsafe_allow_html=True)
    else:
        def get_risk_level(p):
            if p["glucose"] >= 126 or p["cholesterol"] >= 240 or p["haemoglobin"] < 8:
                return "High"
            elif p["glucose"] >= 100 or p["cholesterol"] >= 200 or p["haemoglobin"] < 12:
                return "Moderate"
            return "Low"

        for p in all_patients:
            risk = get_risk_level(p)
            risk_class = {"Low": "risk-low", "Moderate": "risk-moderate", "High": "risk-high"}[risk]
            age = calculate_age(p["date_of_birth"])

            with st.container():
                st.markdown(f"""
                <div class="patient-card">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                        <div>
                            <div class="patient-name">{p['full_name']}</div>
                            <div class="patient-email">{p['email']} · DOB: {p['date_of_birth']} · Age {age}</div>
                        </div>
                        <span class="risk-badge {risk_class}">{risk} Risk</span>
                    </div>
                    <div class="patient-meta">
                        <span class="biomarker-pill">Glucose <span>{p['glucose']} mg/dL</span></span>
                        <span class="biomarker-pill">Haemoglobin <span>{p['haemoglobin']} g/dL</span></span>
                        <span class="biomarker-pill">Cholesterol <span>{p['cholesterol']} mg/dL</span></span>
                    </div>
                    {"<div class='remarks-box'>" + p['remarks'] + "</div>" if p.get('remarks') else ""}
                </div>
                """, unsafe_allow_html=True)

                col_e, col_r, col_d = st.columns([1, 1, 1])
                with col_e:
                    if st.button("✏️ Edit", key=f"edit_{p['id']}", use_container_width=True):
                        st.session_state.edit_patient_id = p['id']
                        st.rerun()
                with col_r:
                    if st.button("🔄 Re-analyse", key=f"reanalyse_{p['id']}", use_container_width=True):
                        with st.spinner("Running AI analysis..."):
                            age_val = calculate_age(p["date_of_birth"])
                            new_remarks = get_health_prediction(p["full_name"], age_val, p["glucose"], p["haemoglobin"], p["cholesterol"])
                            update_patient(p['id'], p['full_name'], p['date_of_birth'], p['email'], p['glucose'], p['haemoglobin'], p['cholesterol'], new_remarks)
                        st.markdown(f'<div class="alert-success">✓ AI assessment updated.</div>', unsafe_allow_html=True)
                        st.rerun()
                with col_d:
                    if st.session_state.confirm_delete_id == p['id']:
                        st.warning("Confirm deletion?")
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("Yes, delete", key=f"confirm_{p['id']}", type="primary"):
                                delete_patient(p['id'])
                                st.session_state.confirm_delete_id = None
                                st.rerun()
                        with c2:
                            if st.button("Cancel", key=f"cancel_{p['id']}"):
                                st.session_state.confirm_delete_id = None
                                st.rerun()
                    else:
                        if st.button("🗑️ Delete", key=f"delete_{p['id']}", use_container_width=True):
                            st.session_state.confirm_delete_id = p['id']
                            st.rerun()

                st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # ── Edit modal ──
        if st.session_state.edit_patient_id:
            p = read_patient_by_id(st.session_state.edit_patient_id)
            if p:
                st.markdown(f"""
                <div class="section-header" style="margin-top:2rem;">
                    <div class="section-title">Edit Patient — {p['full_name']}</div>
                    <div class="section-badge">Editing</div>
                </div>
                """, unsafe_allow_html=True)

                with st.form("edit_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        e_name = st.text_input("Full Name", value=p['full_name'])
                    with col2:
                        e_email = st.text_input("Email", value=p['email'])

                    e_dob = st.date_input("Date of Birth", value=datetime.strptime(p['date_of_birth'], "%Y-%m-%d").date())

                    col3, col4, col5 = st.columns(3)
                    with col3:
                        e_glucose = st.number_input("Glucose", value=float(p['glucose']), step=0.1, format="%.1f")
                    with col4:
                        e_haemoglobin = st.number_input("Haemoglobin", value=float(p['haemoglobin']), step=0.1, format="%.1f")
                    with col5:
                        e_cholesterol = st.number_input("Cholesterol", value=float(p['cholesterol']), step=0.1, format="%.1f")

                    rerun_ai = st.checkbox("Re-generate AI assessment after update", value=True)

                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        save = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                    with col_cancel:
                        cancel = st.form_submit_button("Cancel", use_container_width=True)

                if save:
                    errors = validate_patient_form(e_name, e_dob, e_email, e_glucose, e_haemoglobin, e_cholesterol)
                    if errors:
                        for err in errors:
                            st.markdown(f'<div class="alert-error">⚠️ {err}</div>', unsafe_allow_html=True)
                    else:
                        remarks = p.get('remarks', '')
                        if rerun_ai:
                            with st.spinner("Updating AI analysis..."):
                                age_val = calculate_age(str(e_dob))
                                remarks = get_health_prediction(e_name, age_val, e_glucose, e_haemoglobin, e_cholesterol)
                        success, msg = update_patient(p['id'], e_name, str(e_dob), e_email, e_glucose, e_haemoglobin, e_cholesterol, remarks)
                        if success:
                            st.markdown('<div class="alert-success">✓ Patient record updated successfully.</div>', unsafe_allow_html=True)
                            st.session_state.edit_patient_id = None
                            st.rerun()
                        else:
                            st.markdown(f'<div class="alert-error">⚠️ {msg}</div>', unsafe_allow_html=True)
                if cancel:
                    st.session_state.edit_patient_id = None
                    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# SEARCH
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍  Search":
    st.markdown("""
    <div class="section-header">
        <div class="section-title">Search Patients</div>
        <div class="section-badge">Live Search</div>
    </div>
    """, unsafe_allow_html=True)

    query = st.text_input("Search by name or email", placeholder="Type to search...", label_visibility="collapsed")

    if query:
        results = search_patients(query)
        st.markdown(f'<div class="alert-info">Found {len(results)} result(s) for "{query}"</div>', unsafe_allow_html=True)

        def get_risk_level(p):
            if p["glucose"] >= 126 or p["cholesterol"] >= 240 or p["haemoglobin"] < 8:
                return "High"
            elif p["glucose"] >= 100 or p["cholesterol"] >= 200 or p["haemoglobin"] < 12:
                return "Moderate"
            return "Low"

        for p in results:
            risk = get_risk_level(p)
            risk_class = {"Low": "risk-low", "Moderate": "risk-moderate", "High": "risk-high"}[risk]
            age = calculate_age(p["date_of_birth"])
            st.markdown(f"""
            <div class="patient-card" style="margin-top:0.75rem;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div>
                        <div class="patient-name">{p['full_name']}</div>
                        <div class="patient-email">{p['email']} · Age {age}</div>
                    </div>
                    <span class="risk-badge {risk_class}">{risk} Risk</span>
                </div>
                <div class="patient-meta">
                    <span class="biomarker-pill">Glucose <span>{p['glucose']} mg/dL</span></span>
                    <span class="biomarker-pill">Haemoglobin <span>{p['haemoglobin']} g/dL</span></span>
                    <span class="biomarker-pill">Cholesterol <span>{p['cholesterol']} mg/dL</span></span>
                </div>
                {"<div class='remarks-box'>" + p['remarks'] + "</div>" if p.get('remarks') else ""}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#475569;font-size:0.875rem;padding:1rem 0;">Enter a name or email address to search patient records.</div>', unsafe_allow_html=True)
