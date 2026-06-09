import streamlit as st
import pandas as pd

from resume_parser import extract_text_from_pdf
from matcher import calculate_match_score
from skill_extractor import extract_skills

st.set_page_config(
page_title="AI Resume Screening System",
page_icon="🤖",
layout="wide"
)

st.title("🤖 AI Resume Screening System")

st.caption(
"AI-Powered Applicant Tracking System (ATS)"
)

st.markdown("""
Upload multiple resumes and compare them against a job description.

The system will rank candidates based on their resume match score using AI.
""")

uploaded_resumes = st.file_uploader(
"📄 Upload Resumes (PDF)",
type=["pdf"],
accept_multiple_files=True
)

job_description = st.text_area(
"📝 Paste Job Description",
height=200
)

screen_button = st.button(
"🚀 Screen Resumes",
use_container_width=True
)

st.divider()

if screen_button:

    if not uploaded_resumes:
        st.error("Please upload at least one resume.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:

        with st.spinner("🤖 AI is analyzing resumes..."):

            results = []

            jd_skills = extract_skills(job_description)

            for resume in uploaded_resumes:

                resume_text = extract_text_from_pdf(resume)

                score = calculate_match_score(
                    resume_text,
                    job_description
                )

                resume_skills = extract_skills(
                    resume_text
                )

                matched_skills = []

                for skill in resume_skills:
                    if skill in jd_skills:
                        matched_skills.append(skill)

                missing_skills = []

                for skill in jd_skills:
                    if skill not in resume_skills:
                        missing_skills.append(skill)

                results.append(
                    (
                        resume.name,
                        score,
                        matched_skills,
                        missing_skills
                    )
                )

            results.sort(
                key=lambda x: x[1],
                reverse=True
            )

        st.success(
            "✅ Analysis Completed Successfully!"
        )

        top_score = max(
            result[1]
            for result in results
        )

        average_score = round(
            sum(
                result[1]
                for result in results
            ) / len(results),
            2
        )

        st.subheader("🌟 Top Candidate")

        st.info(
            f"""
🏆 Best Resume: {results[0][0]}

🎯 Match Score: {results[0][1]:.2f}%
"""
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "📄 Total Resumes",
                len(results)
            )

        with col2:
            st.metric(
                "🏆 Top Score",
                f"{top_score:.2f}%"
            )

        with col3:
            st.metric(
                "📊 Average Score",
                f"{average_score:.2f}%"
            )

        df = pd.DataFrame(
            [(r[0], r[1]) for r in results],
            columns=[
                "Resume Name",
                "Match Score"
            ]
        )

        st.download_button(
            label="📥 Download Results as CSV",
            data=df.to_csv(index=False),
            file_name="resume_rankings.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.divider()

        st.subheader("🏆 Resume Rankings")

        for rank, result in enumerate(
            results,
            start=1
        ):

            score = result[1]

            if score >= 80:
                recommendation = "🟢 Highly Recommended"
            elif score >= 60:
                recommendation = "🟡 Recommended"
            else:
                recommendation = "🔴 Needs Improvement"

            with st.container(border=True):

                left, right = st.columns([3, 1])

                with left:

                    if rank == 1:
                        st.subheader("🥇 Rank #1")
                    elif rank == 2:
                        st.subheader("🥈 Rank #2")
                    elif rank == 3:
                        st.subheader("🥉 Rank #3")
                    else:
                        st.subheader(
                            f"Rank #{rank}"
                        )

                    st.write(
                        f"📄 **{result[0]}**"
                    )

                    st.progress(
                        min(int(score), 100)
                    )

                with right:

                    st.metric(
                        "Match Score",
                        f"{score:.2f}%"
                    )

                st.info(
                    recommendation
                )

                col_a, col_b = st.columns(2)

                with col_a:

                    st.markdown(
                        "#### ✅ Matched Skills"
                    )

                    if result[2]:
                        for skill in result[2]:
                            st.write(
                                f"• {skill.title()}"
                            )
                    else:
                        st.write(
                            "No matched skills"
                        )

                with col_b:

                    st.markdown(
                        "#### ❌ Missing Skills"
                    )

                    if result[3]:
                        for skill in result[3]:
                            st.write(
                                f"• {skill.title()}"
                            )
                    else:
                        st.write(
                            "No missing skills"
                        )