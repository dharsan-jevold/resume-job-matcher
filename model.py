import spacy
import subprocess
import importlib
import openai
import json

# --- Load or auto-download spaCy model ---
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    importlib.invalidate_caches()
    nlp = spacy.load("en_core_web_sm")


def extract_entities(text):
    """Extract skills, education, and experience keywords from resume text."""
    doc = nlp(text)
    entities = {
        "skills": [],
        "education": [],
        "experience": [],
    }

    for ent in doc.ents:
        if ent.label_ in ["ORG", "NORP"]:
            entities["education"].append(ent.text)
        elif ent.label_ in ["WORK_OF_ART", "PRODUCT"]:
            entities["skills"].append(ent.text)
        elif ent.label_ in ["DATE"]:
            entities["experience"].append(ent.text)

    return entities


def analyze_resume(resume_text, job_dataset):
    """Find best matching job and suggest related skills."""
    entities = extract_entities(resume_text)

    best_job = None
    best_score = 0

    for job in job_dataset:
        score = 0
        for skill in entities["skills"]:
            if skill.lower() in job["skills"].lower():
                score += 1
        if score > best_score:
            best_score = score
            best_job = job

    # Fallback if no match found
    if not best_job:
        best_job = job_dataset[0]

    # Suggest new skills
    suggested_skills = [
        skill for skill in best_job["skills"].split(", ")
        if skill.lower() not in [s.lower() for s in entities["skills"]]
    ]

    return {
        "best_job": best_job["role"],
        "required_skills": best_job["skills"],
        "suggested_skills": suggested_skills,
    }
