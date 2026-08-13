import os, pickle, numpy as np
from sklearn.ensemble import RandomForestRegressor

class VendorRanker:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=50, random_state=42)
        
    def train(self):
        np.random.seed(42)
        n_samples = 1000

        vendor_prices = np.random.randint(20000, 200000, n_samples)
        user_budgets = np.random.randint(30000, 250000, n_samples)
        ratings = np.random.uniform(3.5, 5.0, n_samples)

        budget_fit = user_budgets - vendor_prices
        over_budget = (vendor_prices > user_budgets).astype(int)

        # High rating + under budget = high score. Over budget = penalty.
        scores = (ratings * 20) + (budget_fit / 5000) - (over_budget * 50)

        X = np.column_stack([budget_fit, over_budget, ratings, vendor_prices])
        self.model.fit(X, scores)

        os.makedirs("models", exist_ok=True)
        with open("models/ranker.pkl", "wb") as f:
            pickle.dump(self.model, f)
        print("[ok] Model Trained.")

    def score_candidates(self, candidates, user_budget):
        with open("models/ranker.pkl", "rb") as f:
            model = pickle.load(f)

        if not candidates:
            return []

        rows = [
            [
                user_budget - c["price"],
                1 if c["price"] > user_budget else 0,
                c["rating"],
                c["price"],
            ]
            for c in candidates
        ]
        predictions = model.predict(np.asarray(rows, dtype=float))

        for idx, score in enumerate(predictions):
            candidates[idx]["ml_score"] = float(score)

        return sorted(candidates, key=lambda x: x["ml_score"], reverse=True)