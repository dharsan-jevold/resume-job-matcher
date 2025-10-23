import fitz 
import spacy
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file."""
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def extract_entities(resume_text):
    """Extract simple skill-like nouns from resume."""
    doc = nlp(resume_text)
    skills = []
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and len(token.text) > 2:
            skills.append(token.text)
    return list(set(skills))

def find_best_job(resume_text, job_dataset):
    """Find the best matching job using cosine similarity."""
    resume_embedding = embed_model.encode(resume_text)
    similarities = []
    for job in job_dataset:
        job_text = " ".join(job["skills"]) + " " + job["role"]
        job_embedding = embed_model.encode(job_text)
        sim = cosine_similarity([resume_embedding], [job_embedding])[0][0]
        similarities.append((job["role"], sim))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[0]

def recommend_skills(job, resume_skills):
    """Suggest missing skills to learn."""
    missing = [s for s in job["skills"] if s.lower() not in [r.lower() for r in resume_skills]]
    return missing

def analyze_resume(pdf_file, job_dataset_path="data/jobs.json"):
    """Full pipeline: extract text → match job → recommend skills."""
    with open(job_dataset_path, "r") as f:
        job_dataset = json.load(f)
    
    text = extract_text_from_pdf(pdf_file)
    extracted_skills = extract_entities(text)
    best_job = find_best_job(text, job_dataset)
    matched_job = next(job for job in job_dataset if job["role"] == best_job[0])
    missing_skills = recommend_skills(matched_job, extracted_skills)

    return {
        "best_job": best_job[0],
        "confidence": round(best_job[1]*100, 2),
        "skills_to_learn": missing_skills,
        "extracted_skills": extracted_skills
    }
