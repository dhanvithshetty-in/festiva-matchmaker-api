import os, json, random

CITIES = ["Mumbai", "Delhi", "Bangalore", "Goa", "Jaipur", "Hyderabad", "Chennai", "Pune"]
CATEGORIES = ["Decorator", "Photographer"]
STYLES = ["Traditional", "Modern", "Luxury", "Minimalist", "Vintage", "Boho", "Royal", "Contemporary", "Outdoor", "Fusion"]

DECORATOR_NAMES = [
    "Aarav & Blossom Studio", "The Bloom Craft", "Saffron Petals", "Vivaah Decor Co.",
    "Luxury Loom Events", "Rosewood Ambiance", "The Marigold House", "Zest Florals",
    "Crimson Choreography", "Silk & Stem", "The Pavilion Studio", "Mehr Decor Studio",
    "Golden Anthurium", "The Tapestry Co.", "Ivy & Ember Events",
]

PHOTOGRAPHER_NAMES = [
    "Shutter Stories Studio", "Frames By Ananya", "Golden Hour Films", "Lens & Light Co.",
    "Candid Chronicles", "The Aperture Atelier", "Lumen Frames", "Sakshi Captures",
    "Pinhole & Beyond", "Everest Exposures", "The Story Gram", "Noor Photography",
    "Focus & Feather", "Timeless Frames Studio", "The Framesmith",
]

DECOR_DESC = "A {style} event decorator in {city}, specializing in bespoke stage design, mandap styling and signature floral installations."
PHOTO_DESC = "Professional {style} photographer in {city}, expert in cinematic wedding portraits, candid storytelling and full event coverage."


def generate_mock_data():
    random.seed(42)
    vendors = []
    i = 0
    for city in CITIES:
        for category in CATEGORIES:
            name_pool = DECORATOR_NAMES if category == "Decorator" else PHOTOGRAPHER_NAMES
            styles = random.sample(STYLES, 6)
            for style in styles:
                i += 1
                name = random.choice(name_pool) + " " + style
                rating = round(random.uniform(3.8, 4.9), 1)
                if category == "Decorator":
                    price = random.randint(30000, 250000)
                else:
                    price = random.randint(20000, 180000)

                desc_template = DECOR_DESC if category == "Decorator" else PHOTO_DESC
                vendors.append({
                    "id": i,
                    "name": name,
                    "category": category,
                    "price": price,
                    "rating": rating,
                    "city": city,
                    "description": desc_template.format(style=style.lower(), city=city),
                })

    os.makedirs("data", exist_ok=True)
    with open("data/vendors.json", "w") as f:
        json.dump(vendors, f, indent=4)
    print(f"[ok] Generated {len(vendors)} synthetic vendors across {len(CITIES)} cities.")


if __name__ == "__main__":
    generate_mock_data()
