import streamlit as st
import requests

# --- PAGE CONFIGURATION & BESPOKE LUXURY THEME ---
st.set_page_config(
    page_title="CAREER ADVANCEMENT PLATFORM",
    page_icon="💼",
    layout="wide"
)

# Custom CSS Injection for the Editorial Sketchbook Aesthetic
st.markdown("""
    <style>
    /* 1. Global Container Control */
    .block-container {
        max-width: 1100px !important;
        padding-top: 4rem !important;
        padding-bottom: 4rem !important;
    }

    /* 2. Butter Yellow Background & Geometric Grid Texture */
    .stApp {
        background-color: #FFECB3;
        background-image: 
            linear-gradient(rgba(15, 44, 89, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(15, 44, 89, 0.04) 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    /* 3. Typography Configuration (Spaced & Sized) */
    h1 {
        font-family: 'Acherone', 'Georgia', serif !important;
        color: #0F2C59 !important;
        text-transform: uppercase;
        font-size: 52px !important;
        letter-spacing: 2px;
        line-height: 1.2 !important;
        white-space: nowrap !important;
        margin-bottom: 25px !important; /* Spacing below main title */
    }

    h2 {
        font-family: 'Acherone', 'Georgia', serif !important;
        color: #0F2C59 !important;
        text-transform: uppercase;
        font-size: 36px !important;
        letter-spacing: 1.5px;
        margin-top: 35px !important;
        margin-bottom: 20px !important;
    }

    h3 {
        font-family: 'Acherone', 'Georgia', serif !important;
        color: #0F2C59 !important;
        text-transform: uppercase;
        font-size: 26px !important;
        letter-spacing: 1px;
        white-space: nowrap !important;
        margin-top: 15px !important;
        margin-bottom: 25px !important;
    }
    
    body, p, label, .stMarkdown {
        font-family: 'Karimun', 'Arial', sans-serif !important;
        color: #1C1C1C !important;
        font-size: 19px !important;
    }
    
    /* 4. Input Boxes Spacing */
    .stTextInput {
        margin-top: 25px !important;
        margin-bottom: 30px !important; /* Added space under target input */
    }

    .stFileUploader {
        margin-top: 25px !important;
        margin-bottom: 25px !important;
    }

    .stTextInput>div>div>input {
        background-color: #F5F5F5 !important;
        border: 2px solid #0F2C59 !important;
        border-radius: 4px !important;
        font-size: 18px !important;
        padding: 12px !important;
    }

    .stFileUploader>div>section {
        background-color: #F5F5F5 !important;
        border: 2px solid #0F2C59 !important;
        border-radius: 4px !important;
    }
    
    /* 5. Clickable Dropdown (Expander) Styling */
    .streamlit-expanderHeader {
        background-color: #F5F5F5 !important;
        border: 2px solid #0F2C59 !important;
        border-radius: 4px !important;
        font-family: 'Acherone', serif !important;
        font-weight: bold !important;
        padding: 15px !important;
    }

    .streamlit-expander {
        margin-bottom: 25px !important; /* Spacing between output boxes */
    }

    .streamlit-expanderHeader p {
        font-size: 18px !important;
        color: #0F2C59 !important;
    }
    
    /* 6. Main Action Button Aesthetic & Placement Spacing */
    .stButton {
        margin-top: 20px !important;
        margin-bottom: 40px !important; /* Generous breathing space below button before output loads */
    }

    .stButton>button {
        background-color: #E1F5FE !important; 
        color: #0F2C59 !important;            
        font-family: 'Acherone', serif !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        font-size: 20px !important;
        letter-spacing: 1.5px !important;
        border: 2px solid #0F2C59 !important;
        padding: 1rem 3rem !important;
        border-radius: 4px !important;
        box-shadow: 4px 4px 0px #0F2C59;       
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #B3E5FC !important; 
        color: #0F2C59 !important;
        box-shadow: 2px 2px 0px #0F2C59;
    }
    
    .stDeployButton, #MainMenu, footer, header {
        visibility: visible !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- MAIN APP LAYOUT ---

st.markdown('<h1>CAREER ADVANCEMENT PLATFORM</h1>', unsafe_allow_html=True)

# Cleaned up, uniformly black instructions with zero emojis and spacious line breaks
st.markdown("""
    <p style="font-size:20px; line-height:1.7; margin-bottom:20px;">
    UPLOAD YOUR RESUME DOWN BELOW AND CHOOSE A TARGET ROLE TO REVIEW YOUR STRENGTHS AND INSIGHTS.<br>
    NOTE: FOR OPTIMAL ACCURACY, PLEASE UTILIZE TEXT-BASED PDF DOCUMENTS GENERATED DIRECTLY VIA MICROSOFT WORD OR CANVA.
    </p>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #0F2C59; margin-bottom:35px;' />", unsafe_allow_html=True)

# Inputs with localized custom margin wrappers applied via CSS rules
uploaded_file = st.file_uploader("UPLOAD RESUME (PDF)", type=["pdf"])
target_job = st.text_input("TARGET ROLE", placeholder="E.G., SPORTS PHYSIOTHERAPIST")

# --- PROFILE PROCESSING & ANALYSIS ---
if st.button("REVIEW MY PROFILE"):
    if uploaded_file is not None and target_job != "":
        with st.spinner("ANALYZING PROFILE STRATEGY..."):
            try:
                file_bytes = uploaded_file.read()
                files = {"file": (uploaded_file.name, file_bytes, "application/pdf")}
                data_payload = {"target_job": target_job}
                backend_url = "http://127.0.0.1:8000/analyze-skills"
                
                response = requests.post(backend_url, data=data_payload, files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    detected_gaps = data.get("detected_gaps", [])
                    action_items = data.get("action_items", [])
                    current_eligibility = data.get("current_eligibility", [])
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.header("CAREER ASSESSMENT")
                    st.markdown(f"<h3>ROLE ASSESSED: {target_job.upper()}</h3>", unsafe_allow_html=True)
                    
                    st.markdown("<hr style='border: 1px solid #0F2C59; margin-bottom:35px;' />", unsafe_allow_html=True)
                    
                    # 1. Target Eligibility
                    with st.expander("☑️ ALIGNED TARGET ELIGIBILITY STATUS", expanded=True):
                        st.markdown("<br>", unsafe_allow_html=True)
                        if isinstance(current_eligibility, list):
                            for role in current_eligibility:
                                st.markdown(f"**Status Assessment:** {str(role)}")
                        else:
                            st.markdown(f"**Status Assessment:** {str(current_eligibility)}")
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.progress(100)
                    
                    # 2. Clickable Dropdown for Skill Gaps
                    with st.expander("🔍 DETECTED SKILL GAPS", expanded=False):
                        st.markdown("<br>", unsafe_allow_html=True)
                        if isinstance(gaps := detected_gaps, list):
                            for gap in gaps:
                                st.markdown(f"• {str(gap)}")
                        else:
                            st.markdown(str(detected_gaps))

                    # 3. Clickable Dropdown for Strategic Action Items
                    with st.expander("🎯 SUGGESTED STRATEGIC ACTION ITEMS", expanded=False):
                        st.markdown("<br>", unsafe_allow_html=True)
                        if isinstance(actions := action_items, list):
                            for action in actions:
                                st.markdown(f"• {str(action)}")
                        else:
                            st.markdown(str(action_items))
                            
                    st.markdown("<br><hr style='border: 0.5px dashed #0F2C59;' />", unsafe_allow_html=True)
                    st.success("ANALYSIS COMPLETE. METRICS SYNCHRONIZED WITH THE CORE ENGINE BACKEND.")
                        
                else:
                    st.error(f"SERVER PIPELINE ERROR: STATUS CODE {response.status_code}")
            except Exception as e:
                st.error(f"CONNECTION OR PARSING ERROR: {str(e)}")
    else:
        st.warning("PLEASE UPLOAD A PDF RESUME AND SPECIFY A TARGET ROLE BEFORE REVIEWING.")