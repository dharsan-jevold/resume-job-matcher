import streamlit as st
from model import analyze_resume

st.set_page_config(page_title="AI Resume Job Matcher", page_icon="💼", layout="wide")

st.title("💼 AI Resume Job Matcher & Skill Recommender")
st.write("Upload your resume and discover the most suitable job roles for you — along with skills to learn.")

uploaded_file = st.file_uploader("📤 Upload your Resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Analyzing your resume... Please wait ⏳"):
        result = analyze_resume(uploaded_file)

    st.success("✅ Resume analyzed successfully!")
    st.subheader("🎯 Best Job Match:")
    st.markdown(f"**{result['best_job']}** (Confidence: {result['confidence']}%)")

    st.subheader("🧠 Skills to Learn / Improve:")
    if result["skills_to_learn"]:
        st.write(", ".join(result["skills_to_learn"]))
    else:
        st.write("You're already skilled for this role! 🌟")

    with st.expander("See Extracted Skills from Resume"):
        st.write(", ".join(result["extracted_skills"]))
else:
    st.info("Please upload a PDF resume to get started.")
