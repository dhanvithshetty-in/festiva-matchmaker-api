from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.orchestrator import MatchmakerOrchestrator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = MatchmakerOrchestrator()

TIERS = [
    {"id": 1, "tier": "Platinum Curation"},
    {"id": 2, "tier": "Gold Curation"},
    {"id": 3, "tier": "Silver Curation"},
]


class MatchRequest(BaseModel):
    city: str
    budget: int
    decorRatio: int


@app.post("/api/curate")
async def curate_package(req: MatchRequest):
    if not (1 <= req.decorRatio <= 99):
        raise ValueError("decorRatio must be between 1 and 99")

    query = "premium luxury wedding decorator and photographer, stage setup, floral, cinematic"
    result = orchestrator.route_and_recommend(
        query, req.city, float(req.budget), decor_ratio=req.decorRatio / 100.0
    )

    combos = result["recommendations"]
    combos = sorted(combos, key=lambda c: c["total_price"], reverse=True)

    bundles = []
    for slot, combo in zip(TIERS, combos):
        dec = combo["decorator"]
        pho = combo["photographer"]
        total = combo["total_price"]
        pitch_lead = {
            1: "Our highest recommendation for {city}.",
            2: "A stunning, balanced alternative for {city}.",
            3: "An exceptional value tier in {city}.",
        }[slot["id"]].format(city=req.city)
        bundles.append(
            {
                "id": slot["id"],
                "tier": slot["tier"],
                "dec": {
                    "name": dec["name"],
                    "price": int(dec["price"]),
                    "rating": dec["rating"],
                    "desc": dec["description"],
                },
                "pho": {
                    "name": pho["name"],
                    "price": int(pho["price"]),
                    "rating": pho["rating"],
                    "desc": pho["description"],
                },
                "pitch": f"{pitch_lead} {combo['explanation']}",
                "total": int(total),
                "savings": max(int(req.budget - total), 0),
            }
        )

    return {"bundles": bundles, "city": req.city}
