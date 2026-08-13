import json, os
import numpy as np
from sentence_transformers import SentenceTransformer

QUERY = "premium luxury wedding decorator and photographer, stage setup, floral, cinematic"

def main():
    with open("data/vendors.json", "r") as f:
        vendors = json.load(f)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    descriptions = [v["description"] for v in vendors]
    embeddings = model.encode(descriptions, convert_to_numpy=True)
    faiss_like = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    np.save("data/vendor_embeddings.npy", faiss_like)

    query_vec = model.encode([QUERY], convert_to_numpy=True)
    query_vec = query_vec / np.linalg.norm(query_vec, axis=1, keepdims=True)
    np.save("data/query_embedding.npy", query_vec)

    print(f"[ok] Saved {faiss_like.shape[0]}x{faiss_like.shape[1]} vendor embeddings + 1x{query_vec.shape[1]} query embedding.")
    print(f"[ok] Total files: {os.path.getsize('data/vendor_embeddings.npy')/1024:.0f} KB + {os.path.getsize('data/query_embedding.npy')/1024:.0f} KB")

if __name__ == "__main__":
    main()
