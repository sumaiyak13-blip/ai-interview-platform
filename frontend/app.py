import streamlit as st
import requests

# 1. SET THE PAGE CONFIG
st.set_page_config(
    page_title="AI Interview Platform", 
    page_icon="💼", 
    layout="centered"
)

# 2. INJECT LUXURY DESIGN WITH BACKGROUND GRAPH TEXTURE
st.markdown("""
    <style>
    /* Global Background (Saturated Butter Yellow + Subtle Fine Drafting Grid) */
    .stApp {
        background-color: #FFECB3 !important; 
        background-image: 
            linear-gradient(rgba(15, 44, 89, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(15, 44, 89, 0.03) 1px, transparent 1px) !important;
        background-size: 24px 24px !important; 
    }
    
    /* Typography Strategy: Karimun for body text */
    html, body, p, div {
        font-family: 'Karimun', 'EB Garamond', serif !important;
        color: #0F2C59 !important; /* Yale Blue */
        font-size: 17px !important;
    }
    
    /* ACHERONE STYLE (ALL CAPS DISPLAY) */
    .acherone-header {
        font-family: 'Acherone', 'Cinzel', serif !important;
        text-transform: uppercase !important;
        color: #0F2C59 !important;
        font-weight: bold !important;
        letter-spacing: 2.5px !important;
    }
    
    /* Apply Acherone to native widget labels */
    [data-testid="stWidgetLabel"] p {
        font-family: 'Acherone', 'Cinzel', serif !important;
        text-transform: uppercase !important;
        font-size: 16px !important;
        color: #0F2C59 !important;
        letter-spacing: 1.5px !important;
    }

    /* VERY LIGHT BLUE ACTION BUTTON */
    div.stButton > button:first-child {
        background-color: #E1F5FE !important; /* Very Light Blue */
        color: #0F2C59 !important; /* Yale Blue Text */
        font-family: 'Acherone', 'Cinzel', serif !important;
        text-transform: uppercase !important;
        font-size: 19px !important;
        font-weight: bold !important;
        letter-spacing: 2px !important;
        border: 2px solid #0F2C59 !important;
        border-radius: 8px !important;
        padding: 0.8rem 2.5rem !important;
        box-shadow: 4px 4px 0px #0F2C59; /* Yale Blue Retro Shadow */
        transition: all 0.15s ease;
        width: 100%;
        margin-top: 10px;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #B3E5FC !important;
        box-shadow: 2px 2px 0px #0F2C59;
    }
    
    div.stButton > button:first-child:active {
        transform: translate(2px, 2px);
        box-shadow: none;
    }
    
    /* COSMOS MARBLE INPUTS */
    div[data-testid="stFileUploader"], div[data-testid="stTextInput"] > div {
        border: 2px solid #0F2C59 !important;
        border-radius: 8px !important;
        background-color: #F5F5F5 !important; /* Cosmos Marble White */
        padding: 5px;
    }
    
    /* DASHBOARD CARD */
    .report-box {
        background-color: #F5F5F5;
        border: 2px solid #0F2C59;
        border-radius: 12px;
        padding: 30px;
        margin-top: 25px;
        box-shadow: 6px 6px 0px #0F2C59;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER & WELCOME
st.markdown('<h1 class="acherone-header">AI INTERVIEW PLATFORM</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size:18px;">✨ Upload your resume and state your dream job to find out where you stand and what to improve.</p>', unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #0F2C59;' />", unsafe_allow_html=True)

# 4. INPUT INTERFACE
st.markdown('<p class="acherone-header" style="font-size:22px; margin-bottom:15px;">📥 INPUTS</p>', unsafe_allow_html=True)

job_description = st.text_input(
    "Target Job Position", 
    placeholder="e.g., Clinical Analyst, Data Scientist..."
)

uploaded_file = st.file_uploader(
    "Upload your CV / Resume", 
    type=["pdf"]
)

# 5. ANALYSIS ENGINE
if st.button("✨ RUN PROFILE ANALYSIS ✨"):
    if job_description and uploaded_file:
        with st.spinner("🧠 Sifting profile patterns..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                data = {"target_job": job_description}  
                
                response = requests.post("http://127.0.0.1:8000/analyze-skills", files=files, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<h2 class="acherone-header" style="font-size:28px;">📊 AI DASHBOARD</h2>', unsafe_allow_html=True)
                    st.markdown('<p class="acherone-header" style="font-size:14px; color:#333;">💡 SKILL INSIGHTS | 🎯 GAP ANALYSIS | ☑️ PERSONALIZED RECOMMENDATIONS</p>', unsafe_allow_html=True)
                    
                    # --- UNPACKING BACKEND DICTIONARY SAFELY ---
                    # We handle strings or lists cleanly so nothing breaks
                    gaps = result.get("detected_gaps", "None identified.")
                    actions = result.get("action_items", "None identified.")
                    eligibility = result.get("current_eligibility", "Not analyzed.")
                    
                    # Convert lists to clean strings with spacing if the backend returns lists
                    if isinstance(gaps, list): gaps = "<br>• ".join(gaps)
                    if isinstance(actions, list): actions = "<br>• ".join(actions)
                    if isinstance(eligibility, list): eligibility = ", ".join(eligibility)
                    
                    # Formatting the text layout cleanly inside our Cosmos Marble box
                    report_html = f"""
                    <div class="report-box">
                        <p style="font-size: 18px; margin-bottom: 15px;"><b>🎯 Target Position:</b> {job_description.upper()}</p>
                        <hr style="border: 0.5px dashed #0F2C59; margin-bottom: 15px;">
                        <p style="margin-bottom: 12px;"><b>📋 Current Eligibility Rating:</b><br>{eligibility}</p>
                        <p style="margin-bottom: 12px;"><b>🔍 Detected Skill Gaps:</b><br>• {gaps}</p>
                        <p style="margin-bottom: 0px;"><b>💡 Personalized Action Items:</b><br>• {actions}</p>
                    </div>
                    """
                    st.markdown(report_html, unsafe_allow_html=True)
                else:
                    st.error("❌ Processing Failure. Check Backend.")
            except Exception as e:
                st.error("🔌 Connection Error. Wake up the backend server.")
    else:
        st.warning("⚠️ Supply a job title and a PDF resume first.")