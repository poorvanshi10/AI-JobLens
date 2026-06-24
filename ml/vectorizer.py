from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ResumeVectorizer:
    """
    Converts unstructured text into TF-IDF vector space matrices 
    to calculate semantic cosine similarity.
    """
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),  # Captures phrases like "natural language processing"
            max_features=5000
        )

    def calculate_similarity(self, resume_text: str, jd_text: str) -> float:
        try:
            # Fit and transform texts into high-dimensional vectors
            tfidf_matrix = self.vectorizer.fit_transform([resume_text, jd_text])
            
            # Calculate the geometric angle (similarity) between the two vectors
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            return float(similarity_matrix[0][0])
        except Exception as e:
            print(f"Vectorization Error: {e}")
            return 0.0
