import streamlit as st
from resume_parser import extract_text_from_pdf
from matcher import calculate_match_score

st.title("AI Resume Screener")

uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description"
)

if uploaded_resume and job_description:

    resume_text = extract_text_from_pdf(uploaded_resume)

    score = calculate_match_score(
        resume_text,
        job_description
    )

    st.subheader("Resume Match Score")

    st.success(f"{score}%")