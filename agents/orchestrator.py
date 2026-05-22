from models.embedding_search import EmbeddingSearcher
from models.ranking_model import VendorRanker

class RankingAgent:
    """Agent 2: Scores candidate vendors using the ML model with business-weighted budgets."""

    def __init__(self, ranker: VendorRanker):
        self.ranker = ranker

    def run(
        self,
        candidates: dict[str, list[dict]],
        budget: float,
        top_k: int,
        trace: list[str],
    ) -> dict[str, list[dict]]:
        trace.append(f"[RankingAgent] Analyzing market segments for budget ₹{budget:,.0f} …")

        ranked: dict[str, list[dict]] = {}
        
        if "Decorator" in candidates and "Photographer" in candidates:
            budget_allocations = {
                "Decorator": budget * 0.60,
                "Photographer": budget * 0.40
            }
            trace.append("[RankingAgent] Applying weighted allocation: 60% Decor / 40% Photography.")
        else:
            n_cats = len(candidates)
            per_cat_budget = budget / max(n_cats, 1)
            budget_allocations = {cat: per_cat_budget for cat in candidates}

        for cat, vendors in candidates.items():
            cat_budget = budget_allocations.get(cat, budget / 2)
            scored = self.ranker.score_candidates(vendors, cat_budget)
            ranked[cat] = scored[:top_k]
            trace.append(
                f"[RankingAgent] Top {cat} candidates evaluated against target segment budget of ₹{cat_budget:,.0f}."
            )

        return ranked


class MatchmakerOrchestrator:
    """Coordinates the full Multi-Agent pipeline for Festiva Moments."""
    
    def __init__(self):
        self.searcher = EmbeddingSearcher()
        self.searcher.build_index()# Loads data & index safely
        
        self.ranker = VendorRanker()
        # Initialize our ranking agent wrapper
        self.ranking_agent = RankingAgent(self.ranker)

    def route_and_recommend(self, query: str, city: str, total_budget: float):
        trace = []
        
        # -------------------------------------------------------------
        # Agent 1: Matching (Semantic Retrieval)
        # -------------------------------------------------------------
        trace.append("Matching Agent: Finding semantically relevant vendors...")
        
        decorators = self.searcher.search(query, city, "Decorator", top_k=5)
        photographers = self.searcher.search(query, city, "Photographer", top_k=5)
        
        # Package retrieved sets into a unified candidate map for Agent 2
        candidates = {
            "Decorator": decorators,
            "Photographer": photographers
        }
        
        # -------------------------------------------------------------
        # Agent 2: Ranking (ML Scoring with Business Rules)
        # -------------------------------------------------------------
        trace.append("Ranking Agent: Applying ML scores with industry-weighted budget constraints...")
        ranked_output = self.ranking_agent.run(candidates, total_budget, top_k=3, trace=trace)
        
        ranked_decorators = ranked_output.get("Decorator", [])
        ranked_photographers = ranked_output.get("Photographer", [])
        
        # -------------------------------------------------------------
        # Agent 3: Evaluation & Explanation
        # -------------------------------------------------------------
        trace.append("Explanation Agent: Pairing best high-value combinations...")
        combinations = []
        
        for dec in ranked_decorators:
            for pho in ranked_photographers:
                total_cost = dec["price"] + pho["price"]
                
                # Check absolute budget ceiling constraint
                if total_cost <= total_budget:
                    explanation = f"Great fit for {city}! Total bundle cost is ₹{total_cost:,}, safely within your ₹{total_budget:,} budget parameters."
                    combinations.append({
                        "decorator": dec,
                        "photographer": pho,
                        "total_price": total_cost,
                        "combined_score": dec["ml_score"] + pho["ml_score"],
                        "explanation": explanation
                    })
        
        # Sort packages by best joint mathematical score
        combinations = sorted(combinations, key=lambda x: x["combined_score"], reverse=True)[:3]
        return {"recommendations": combinations, "agent_trace": trace}