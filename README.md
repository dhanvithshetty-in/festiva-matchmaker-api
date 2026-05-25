# Festiva Moments | Agentic AI Engine (Backend)

📖 **Live API Docs (Swagger):** https://festiva-matchmaker-api.onrender.com/docs

<img width="1920" height="1080" alt="ai matchmaker gi" src="https://github.com/user-attachments/assets/a08cf110-57ab-4ff3-9075-c0955f2e4a46" />


This is the central "brain" of the Festiva Moments application. It is a cloud-native REST API that utilizes a custom Retrieval-Augmented Generation (RAG) pipeline to match users with luxury event vendors based on high-dimensional semantic search and AI synthesis.

## 🧠 Architecture & Tech Stack
* **Framework:** FastAPI (Python)
* **Vector Database:** FAISS (Facebook AI Similarity Search)
* **Embeddings:** `sentence-transformers` (PyTorch)
* **LLM Integration:** Google Gemini API
* **Containerization:** Docker
* **Deployment:** Render 

## ⚙️ The RAG Pipeline Workflow
1. **Retrieval:** The API receives constraints (budget, city, allocation). It queries a local FAISS vector store containing 2,400+ vendor embeddings to find the mathematically closest matches.
2. **Augmentation:** The mathematically optimized vendor pairs (Decor + Photography) are formatted into strict JSON data schemas.
3. **Generation:** An Agentic AI prompt containing the vendor data and user constraints is sent to the Gemini API, which synthesizes a personalized luxury marketing pitch for the bundle.

## 💻 Local Development

1. Clone the repository:
   ```bash
   git clone [https://github.com/dhanvithshetty-in/festiva-matchmaker-api.git](https://github.com/dhanvithshetty-in/festiva-matchmaker-api.git)
   cd festiva-matchmaker-api
