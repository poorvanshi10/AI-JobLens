import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="AI-JobLens Engine")

# Enable CORS so the Chrome Extension can talk to your localhost API securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Reference taxonomy for entity mapping
SKILL_TAXONOMY = [
    "python", "machine learning", "deep learning", "nlp", "natural language processing",
    "fastapi", "flask", "django", "sql", "mongodb", "typescript", "javascript", 
    "pytorch", "tensorflow", "scikit-learn", "git", "github", "docker", "aws", "data structures"
]

class MatchRequest(BaseModel):
    resume_text: str
    job_description: str

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s#\+]', '', text)
    return text

@app.post("/match-resume")
async def match_resume(payload: MatchRequest):
    cleaned_resume = clean_text(payload.resume_text)
    cleaned_jd = clean_text(payload.job_description)

    # 1. Context Vectorization & Cosine Similarity via Scikit-Learn
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([cleaned_resume, cleaned_jd])
    similarity_res = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    base_similarity_score = int(similarity_res[0][0] * 100)

    # 2. NLP Taxonomy Match Extraction
    extracted_jd_skills = [skill for skill in SKILL_TAXONOMY if skill in cleaned_jd]
    extracted_resume_skills = [skill for skill in SKILL_TAXONOMY if skill in cleaned_resume]

    missing_skills = [s.title() for s in extracted_jd_skills if s not in extracted_resume_skills]
    matched_skills = [s.title() for s in extracted_jd_skills if s in extracted_resume_skills]

    # Calculate final blended match score
    total_jd_skills = len(extracted_jd_skills)
    if total_jd_skills > 0:
        skill_coverage = (len(matched_skills) / total_jd_skills) * 100
        final_score = int((base_similarity_score * 0.4) + (skill_coverage * 0.6))
    else:
        final_score = base_similarity_score

    final_score = min(max(final_score, 15), 98)

    # 3. Dynamic Job Classification
    role = "Software Engineer"
    if any(x in cleaned_jd for x in ["ml", "machine learning", "deep learning", "nlp"]):
        role = "AI/ML Engineer / Intern"
    elif "data science" in cleaned_jd or "data scientist" in cleaned_jd:
        role = "Data Scientist"
    elif any(x in cleaned_jd for x in ["fullstack", "frontend", "typescript"]):
        role = "Full-Stack Developer"

    # 4. Recommendation Generation Engine Loop
    recommendations = []
    if missing_skills:
        recommendations.append(f"Incorporate missing core skills explicitly: {', '.join(missing_skills[:3])}.")
    if "fastapi" in missing_skills or "sql" in missing_skills:
        recommendations.append("Build and host a public REST API endpoint to demonstrate backend architecture execution.")
    if final_score < 75:
        recommendations.append("Revise project formatting structures to showcase clear performance metrics.")
    else:
        recommendations.append("High alignment detected! Customize metrics and apply confidently.")

    return {
        "role_detected": role,
        "match_score": final_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills[:6],
        "recommendations": recommendations
    }
