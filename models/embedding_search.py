import json, os, numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class EmbeddingSearcher:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.vendors = []
        
    def build_index(self):
        with open("data/vendors.json", "r") as f:
            self.vendors = json.load(f)
            
        descriptions = [v["description"] for v in self.vendors]
        embeddings = self.model.encode(descriptions, convert_to_numpy=True)
        faiss.normalize_L2(embeddings)
        
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)
        print("[ok] FAISS index built.")
        
    def search(self, query: str, city: str, category: str, top_k: int = 10):
        query_vector = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_vector)
        
        distances, indices = self.index.search(query_vector, len(self.vendors))
        results = []
        
        for score, idx in zip(distances[0], indices[0]):
            vendor = self.vendors[idx]
            if vendor["city"].lower() == city.lower() and vendor["category"].lower() == category.lower():
                v_copy = vendor.copy()
                v_copy["similarity_score"] = float(score)
                results.append(v_copy)
                if len(results) >= top_k:
                    break
        return results