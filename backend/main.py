from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ml.preprocessing import TextPreprocessor
from ml.vectorizer import ResumeVectorizer
from ml.scoring_model import JobFitScoringModel

app = FastAPI(title="AI-JobLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Robust ATS Skill Dictionary
SKILL_TAXONOMY = [
    "python", "machine learning", "deep learning", "nlp", "natural language processing",
    "fastapi", "flask", "django", "sql", "mongodb", "typescript", "javascript", 
    "pytorch", "tensorflow", "scikit learn", "git", "github", "docker", "aws", 
    "data structures", "pandas", "numpy", "spacy", "rest api", "deployment"
]

class MatchRequest(BaseModel):
    resume_text: str
    job_description: str

# Boot up ML models
preprocessor = TextPreprocessor()
vectorizer = ResumeVectorizer()
scoring_engine = JobFitScoringModel(taxonomy=SKILL_TAXONOMY)

@app.post("/match-resume")
async def match_resume(payload: MatchRequest):
    # 1. Clean and Lemmatize
    cleaned_resume = preprocessor.clean(payload.resume_text)
    cleaned_jd = preprocessor.clean(payload.job_description)

    # 2. Vector Similarity Score (TF-IDF + Cosine)
    base_similarity_metric = vectorizer.calculate_similarity(cleaned_resume, cleaned_jd)
    base_score = int(base_similarity_metric * 100)

    # 3. Taxonomy Gap Analysis
    gap_data = scoring_engine.perform_gap_analysis(cleaned_resume, cleaned_jd)
    
    total_req = gap_data["total_required_count"]
    if total_req > 0:
        coverage_score = (len(gap_data["matched"]) / total_req) * 100
        # Blend contextual semantic score with exact skill matches
        final_score = int((base_score * 0.35) + (coverage_score * 0.65))
    else:
        final_score = base_score

    final_score = min(max(final_score, 12), 98)

    # 4. Predict Role
    predicted_role = scoring_engine.predict_role_category(cleaned_jd)

    # 5. Generate AI Recommendations
    recommendations = []
    missing = gap_data["missing"]
    
    if missing:
        recommendations.append(f"Add missing core skills: {', '.join(missing[:3])}.")
    if "Fastapi" in missing or "Mongodb" in missing:
        recommendations.append("Build a REST API to demonstrate backend capabilities.")
    if final_score < 70:
        recommendations.append("Increase exact ATS keyword density for better filtering results.")
    else:
        recommendations.append("High alignment! Tailor your project impact metrics and apply.")

    return {
        "role_detected": predicted_role,
        "match_score": final_score,
        "matched_skills": gap_data["matched"],
        "missing_skills": missing[:6],
        "recommendations": recommendations
    }
