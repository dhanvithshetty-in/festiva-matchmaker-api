from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MatchRequest(BaseModel):
    city: str
    budget: int
    decorRatio: int

@app.post("/api/curate")
async def curate_package(req: MatchRequest):
    # In production, this loops through your FAISS top_k=3 results
    # We are calculating dynamic prices based on the user's budget input
    
    bundles = [
        {
            "id": 1,
            "tier": "Platinum Curation",
            "dec": {"name": "Royal Knot Weddings", "price": int(req.budget * 0.55), "rating": 4.9, "desc": "Bespoke palatial stage designs and luxury floral mandaps."},
            "pho": {"name": "Cinematic Captures", "price": int(req.budget * 0.35), "rating": 4.8, "desc": "Award-winning aerial drone cinematography and candid portraiture."},
            "pitch": "Our highest recommendation. This pairing offers unparalleled visual grandeur and elite documentation, perfectly optimized to maximize your investment.",
            "total": int(req.budget * 0.90),
            "savings": int(req.budget * 0.10)
        },
        {
            "id": 2,
            "tier": "Gold Curation",
            "dec": {"name": "Heritage Elegance", "price": int(req.budget * 0.50), "rating": 4.7, "desc": "Traditional cultural motifs fused with a refined, modern editorial aesthetic."},
            "pho": {"name": "Golden Hour Films", "price": int(req.budget * 0.30), "rating": 4.9, "desc": "Renowned specialists in the art of golden-hour portraiture and sweeping films."},
            "pitch": "A stunning alternative that balances heritage design with luminous photography, leaving a healthy contingency margin in your budget.",
            "total": int(req.budget * 0.80),
            "savings": int(req.budget * 0.20)
        },
        {
            "id": 3,
            "tier": "Silver Curation",
            "dec": {"name": "Blooming Celebrations", "price": int(req.budget * 0.45), "rating": 4.6, "desc": "Sustainable, garden-inspired floral installations with a highly organic feel."},
            "pho": {"name": "Frame & Feel Studio", "price": int(req.budget * 0.25), "rating": 4.7, "desc": "Intimate storytelling with highly editorial precision and color grading."},
            "pitch": "An exceptional value tier that prioritizes organic aesthetics and timeless editorial storytelling while retaining significant capital.",
            "total": int(req.budget * 0.70),
            "savings": int(req.budget * 0.30)
        }
    ]
    
    return {"bundles": bundles}