import streamlit as st
from llama_index.core.llama_pack import download_llama_pack
import openai
import os

# Function to screen the resume based on provided job description
def screen_resume(job_description, resume_path, api_key):
    # Set the OpenAI API key
    openai.api_key = api_key
    
    # Download the Resume Screener Pack
    ResumeScreenerPack = download_llama_pack("ResumeScreenerPack", "./resume_screener_pack")
    resume_screener = ResumeScreenerPack(
        job_description=job_description,
        criteria=[]  # Assuming criteria are included within the job description itself
    )
    
    # Run the screening process
    response = resume_screener.run(resume_path=resume_path)
    overall_reasoning = f"Reasoning: {str(response.overall_reasoning)}"
    overall_decision = f"Decision: {str(response.overall_decision)}"
    
    # Determine overall assessment
    if str(response.overall_decision).lower() == 'yes':
        overall_assessment = "Overall Assessment: Good Fit"
    elif str(response.overall_decision).lower() == 'maybe':
        overall_assessment = "Overall Assessment: Partial Fit"
    else:
        overall_assessment = "Overall Assessment: Not a Good Fit"
    
    return overall_reasoning, overall_decision, overall_assessment

# Streamlit App

st.title("Resume Screening App")

# API Key input
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

st.subheader("Job Description")
job_description = st.text_area("Enter the job description here")

st.subheader("Upload Resume")
uploaded_file = st.file_uploader("Upload a resume (PDF format)", type="pdf")

if st.button("Screen Resume"):
    if job_description and uploaded_file and api_key:
        # Save uploaded resume
        with open("uploaded_resume.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Run the resume screening function
        reasoning, decision, assessment = screen_resume(job_description, "uploaded_resume.pdf", api_key)
        
        # Display results
        st.write(reasoning)
        st.write(decision)
        st.write(assessment)
    else:
        st.error("Please provide the job description, a resume, and your API key.")
