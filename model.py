import fitz 
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    return text


def analyze_resume(text):
    text = clean_text(text)

    job_skills = {
        "Data Scientist": ["python", "machine learning", "statistics", "data analysis", "pandas", "numpy"],
        "Web Developer": ["html", "css", "javascript", "react", "node", "frontend", "backend"],
        "AI Engineer": ["deep learning", "neural network", "tensorflow", "pytorch", "nlp"],
        "Software Engineer": ["java", "c++", "git", "sql", "software design", "algorithms"],
        "Data Analyst": ["excel", "sql", "powerbi", "data visualization", "statistics"],
        "Cloud Engineer": ["aws", "azure", "docker", "kubernetes", "devops"],
        "Cybersecurity Analyst": ["network security", "linux", "firewall", "encryption", "incident response"]
    }

    vectorizer = TfidfVectorizer()
    resume_vec = vectorizer.fit_transform([text])
    job_scores = {}

    for job, skills in job_skills.items():
        skill_text = " ".join(skills)
        job_vec = vectorizer.transform([skill_text])
        score = cosine_similarity(resume_vec, job_vec)[0][0]
        job_scores[job] = round(float(score), 3)

    best_match = max(job_scores, key=job_scores.get)
    return best_match, job_scores, job_skills[best_match]
