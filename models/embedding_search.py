import json, os
import numpy as np
import faiss


class EmbeddingSearcher:
    """Vector search over precomputed vendor embeddings (no ML model at runtime).

    Vendor + query embeddings are computed offline (data/precompute_embeddings.py)
    and loaded from disk, so the API stays fast and lightweight on small instances.
    """

    def __init__(self):
        self.index = None
        self.vendors = []
        self.query_vector = None

    def build_index(self):
        with open("data/vendors.json", "r") as f:
            self.vendors = json.load(f)

        embeddings = np.load("data/vendor_embeddings.npy")
        self.query_vector = np.load("data/query_embedding.npy")

        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)
        print("[ok] FAISS index built from precomputed embeddings.")

    def search(self, query: str, city: str, category: str, top_k: int = 10):
        distances, indices = self.index.search(self.query_vector, len(self.vendors))
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
