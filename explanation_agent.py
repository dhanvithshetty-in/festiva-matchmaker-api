import os
from google import genai
from google.genai import types

# Initialize the client using an environment variable named GEMINI_API_KEY.
# Do not store API keys directly in source control.
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise EnvironmentError("Missing GEMINI_API_KEY environment variable")
client = genai.Client(api_key=gemini_api_key)

def generate_pitch(city: str, total_budget: float, decorator: dict, photographer: dict) -> str:
    """Uses the new Google GenAI SDK to write a personalized sales pitch."""
    
    total_cost = decorator['price'] + photographer['price']
    savings = total_budget - total_cost
    
    prompt = f"""
    You are an elite, highly persuasive wedding planner AI working for Festiva Moments.
    A client wants to plan an event in {city} with a strict total budget of ₹{total_budget}.
    
    You have mathematically optimized the perfect vendor package for them:
    
    🎨 DECORATOR: {decorator['name']} (Cost: ₹{decorator['price']} | Rating: ⭐{decorator['rating']})
    Details: {decorator['description']}
    
    📸 PHOTOGRAPHER: {photographer['name']} (Cost: ₹{photographer['price']} | Rating: ⭐{photographer['rating']})
    Details: {photographer['description']}
    
    FINANCIALS: Total package cost is ₹{total_cost}. This saves the client ₹{savings} under their budget limit!
    
    YOUR TASK: 
    Write a short, punchy, 2-to-3 sentence explanation for the client on WHY you selected this specific combination. 
    Connect the specific details of the vendors together. Sound professional, confident, and highlight the financial value.
    Do NOT use asterisks, bolding, or markdown formatting. Keep it plain text.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ LLM Generation failed: {e}")
        return f"Great fit for {city}! Total bundle cost is ₹{total_cost}, safely within your budget parameters."

if __name__ == "__main__":
    dec = {"name": "Royal Knot", "price": 120000, "rating": 4.8, "description": "Luxury floral mandaps."}
    pho = {"name": "Candid Captures", "price": 60000, "rating": 4.9, "description": "Cinematic wedding experts."}
    
    print("🤖 AI is thinking using the modern google-genai SDK...")
    pitch = generate_pitch("Mumbai", 200000, dec, pho)
    print("\n💡 EXPLANATION AGENT SAYS:")
    print(pitch)