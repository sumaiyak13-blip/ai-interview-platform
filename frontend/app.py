import streamlit as st
import requests

st.set_page_config(page_title="AI Interview Platform", layout="wide")

st.title("🤖 AI Interview Platform")
st.markdown("---")

st.header("🔍 Intelligent Skill Gap & Eligibility Analyzer")
st.write("Upload your resume and state your dream job to find out where you stand and what to improve.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Inputs")
    job_input = st.text_input("Target Job Position", placeholder="e.g., Data Scientist, Backend Developer")
    uploaded_file = st.file_uploader("Upload your CV / Resume", type=["pdf"])
    submit_btn = st.button("Analyze My Profile", type="primary")

with col2:
    st.subheader("AI Analysis Dashboard")
    
    if submit_btn:
        if not job_input or not uploaded_file:
            st.error("Please provide both a target job position and upload a PDF resume.")
        else:
            with st.spinner("Analyzing profile patterns and career paths..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    data = {"target_job": job_input}
                    
                    # Connects directly to your backend endpoint "/analyze-skills"
                    response = requests.post("http://localhost:8000/analyze-skills", data=data, files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"Analysis completed for target role: **{result['target_job']}**")
                        
                        st.warning("⚠️ **Identified Skill Gaps & Missing Blocks**")
                        for gap in result["detected_gaps"]:
                            st.write(f"- {gap}")
                            
                        st.info("💡 **Recommended Action Plan**")
                        for item in result["action_items"]:
                            st.write(f"- {item}")
                            
                        st.success("💼 **Roles You are Currently Eligible For**")
                        for role in result["current_eligibility"]:
                            st.write(f"✅ {role}")
                    else:
                        st.error("Backend processing failed.")
                except Exception as e:
                    st.error(f"Could not connect to the backend server. Exception: {e}")