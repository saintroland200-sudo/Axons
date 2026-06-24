import re
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class TokenOptimizer:
    def __init__(self):
        pass

    # Engine 1: Extractive Summarization (TF-IDF based)
    def compress_extractive(self, text: str, ratio: float = 0.5) -> str:
        sentences = re.split(r'(?<=[.!?]) +', text)
        if len(sentences) <= 2:
            return text

        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(sentences)
            scores = np.asarray(tfidf_matrix.sum(axis=1)).flatten()

            num_sentences = max(1, int(len(sentences) * ratio))
            top_indices = np.argsort(scores)[-num_sentences:]
            top_indices.sort()

            return " ".join([sentences[i] for i in top_indices])
        except Exception:
            return text

    # Engine 2: Keyword Extraction
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([text])
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.toarray().flatten()

            top_indices = np.argsort(scores)[-top_n:]
            return [feature_names[i] for i in top_indices[::-1]]
        except Exception:
            return []

    # Engine 3: Semantic Compression (Simplified: Dedup sentences)
    def compress_semantic(self, text: str) -> str:
        sentences = re.split(r'(?<=[.!?]) +', text)
        seen = set()
        unique_sentences = []
        for s in sentences:
            clean = s.strip().lower()
            if clean not in seen:
                seen.add(clean)
                unique_sentences.append(s)
        return " ".join(unique_sentences)

    # Engine 4: Query-Aware Truncation
    def truncate_query_aware(self, text: str, query: str, max_chars: int = 500) -> str:
        if not query or query.lower() not in text.lower():
            return text[:max_chars]

        # Find query and take context around it
        idx = text.lower().find(query.lower())
        start = max(0, idx - max_chars // 2)
        end = min(len(text), start + max_chars)
        return "..." + text[start:end] + "..."

if __name__ == "__main__":
    opt = TokenOptimizer()
    sample = "The LAIS system is a multi-agent system. It uses an ACP bus for communication. The system is designed to be robust. Communication is key in LAIS."
    print(f"Extractive: {opt.compress_extractive(sample, 0.5)}")
    print(f"Keywords: {opt.extract_keywords(sample)}")
