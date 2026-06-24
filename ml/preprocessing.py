import re
import spacy

class TextPreprocessor:
    """
    Production NLP pipeline using spaCy for tokenization, 
    stop-word removal, and lemmatization.
    """
    def __init__(self):
        # Keeps technical terms intact (C++, .NET) while stripping layout clutter
        self.clean_regex = re.compile(r'[^a-z0-9\s#\+\-\.]')
        
        # Load spaCy NLP model (Downloads automatically if missing)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            import spacy.cli
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def clean(self, raw_text: str) -> str:
        if not raw_text:
            return ""
        
        # Lowercase and regex sanitize
        text = self.clean_regex.sub(' ', raw_text.lower())
        
        # Process through spaCy pipeline
        doc = self.nlp(text)
        
        # Extract lemmas (root words) and remove stop words (and, the, is)
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_space]
        
        return " ".join(tokens)
