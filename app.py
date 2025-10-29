import streamlit as st
import matplotlib.pyplot as plt
from model import extract_text_from_pdf, analyze_resume

st.set_page_config(page_title="Resume Job Matcher", page_icon="🧠", layout="wide")

st.title("🧠 Resume Job Matcher")
st.markdown("Upload your resume and discover your best career fit!")

uploaded_file = st.file_uploader("📄 Upload your Resume (PDF only)", type=["pdf"])

if uploaded_file:
    with st.spinner("Analyzing your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        best_match, job_scores, best_skills = analyze_resume(resume_text)

    st.success(f"### ✅ Best Job Match: **{best_match}**")

    # --- Visualization 1: Bar Chart for all job match scores ---
    st.subheader("📊 Job Match Percentage")
    jobs = list(job_scores.keys())
    scores = [v * 100 for v in job_scores.values()]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(jobs, scores, color='skyblue')
    ax.set_xlabel("Match Percentage (%)")
    ax.set_ylabel("Job Role")
    ax.set_xlim(0, 100)
    ax.invert_yaxis()
    ax.set_title("Resume Match vs Job Roles", fontsize=12)
    st.pyplot(fig)

    # --- Visualization 2: Pie Chart for skill importance ---
    st.subheader(f"🧩 Key Skills for {best_match}")
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    ax2.pie(
        [1] * len(best_skills),
        labels=best_skills,
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Paired.colors
    )
    ax2.set_title("Skill Importance Breakdown", fontsize=12)
    st.pyplot(fig2)

    st.info("💡 Tip: Learn or improve on these key skills to boost your profile for this role.")
else:
    st.info("👆 Upload a PDF resume to get started.")
