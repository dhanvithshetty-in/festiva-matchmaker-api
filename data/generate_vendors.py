import os, json, random

CITIES = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Pune"]
CATEGORIES = ["Decorator", "Photographer"]
STYLES = ["Traditional", "Modern", "Luxury", "Minimalist", "Vintage"]

def generate_mock_data():
    vendors = []
    for i in range(1, 101):
        category = random.choice(CATEGORIES)
        city = random.choice(CITIES)
        style = random.choice(STYLES)
        rating = round(random.uniform(3.5, 5.0), 1)
        
        if category == "Decorator":
            price = random.randint(30000, 250000)
            desc = f"A {style.lower()} event decorator in {city}, specializing in beautiful stage setups and floral arrangements."
        else:
            price = random.randint(20000, 180000)
            desc = f"Professional {style.lower()} photographer in {city}. Expert in cinematic wedding portraits and event coverage."

        vendors.append({
            "id": i,
            "name": f"{style} {category} {i}",
            "category": category,
            "price": price,
            "rating": rating,
            "city": city,
            "description": desc
        })
        
    os.makedirs("data", exist_ok=True)
    with open("data/vendors.json", "w") as f:
        json.dump(vendors, f, indent=4)
    print("✓ Generated 100 synthetic vendors.")

if __name__ == "__main__":
    generate_mock_data()