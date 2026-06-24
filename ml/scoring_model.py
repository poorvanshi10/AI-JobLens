from typing import List, Dict, Any

class JobFitScoringModel:
    """
    Evaluates skill overlaps, detects missing entities, and classifies job roles.
    """
    def __init__(self, taxonomy: List[str]):
        self.taxonomy = taxonomy

    def perform_gap_analysis(self, cleaned_resume: str, cleaned_jd: str) -> Dict[str, Any]:
        extracted_jd_skills = [skill for skill in self.taxonomy if skill in cleaned_jd]
        extracted_resume_skills = [skill for skill in self.taxonomy if skill in cleaned_resume]

        missing_skills = [s.title() for s in extracted_jd_skills if s not in extracted_resume_skills]
        matched_skills = [s.title() for s in extracted_jd_skills if s in extracted_resume_skills]

        return {
            "matched": matched_skills,
            "missing": missing_skills,
            "total_required_count": len(extracted_jd_skills)
        }

    def predict_role_category(self, cleaned_jd: str) -> str:
        # Context-aware classifier
        if any(x in cleaned_jd for x in ["ml", "machine learning", "deep learning", "nlp", "spacy", "tensorflow"]):
            return "AI/ML Engineer"
        elif any(x in cleaned_jd for x in ["data science", "data scientist", "pandas", "numpy"]):
            return "Data Scientist"
        elif any(x in cleaned_jd for x in ["fullstack", "react", "node", "typescript"]):
            return "Full-Stack Developer"
        return "Software Engineer"
