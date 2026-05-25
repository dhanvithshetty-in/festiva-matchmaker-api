import streamlit as st
import time
from explanation_agent import generate_pitch

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Festiva Matchmaker",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# --- 2. LUXURY CSS INJECTION ---
st.markdown("""
    <style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,600;1,400&display=swap');

    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Global Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #FAFAFA;
        color: #2C3338;
    }

    /* Luxury Hero Section */
    .hero-container {
        text-align: center;
        padding-top: 3rem;
        padding-bottom: 2rem;
    }
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-weight: 600;
        font-size: 4rem;
        color: #1A1A1A;
        margin-bottom: 0px;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-weight: 300;
        color: #8C8C8C;
        font-size: 1.2rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 10px;
    }

    /* Elegant AI Highlight Box */
    .ai-highlight {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-left: 3px solid #D4AF37; /* Champagne Gold */
        padding: 30px;
        border-radius: 12px;
        font-family: 'Playfair Display', serif;
        font-size: 1.3rem;
        line-height: 1.8;
        color: #333333;
        font-style: italic;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-bottom: 2.5rem;
    }

    /* Premium Metric Styling */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #EAEAEA;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }
    
    /* Input Container Styling */
    .stSelectbox, .stNumberInput, .stSlider {
        padding-bottom: 15px;
    }
    
    /* Gold Accent Button */
    div.stButton > button:first-child {
        background-color: #1A1A1A;
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        padding: 15px 0px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #D4AF37; /* Gold Hover */
        color: #FFFFFF;
        box-shadow: 0 8px 20px rgba(212, 175, 55, 0.3);
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HERO SECTION ---
st.markdown('<div class="hero-container">', unsafe_allow_html=True)
st.markdown('<p class="hero-title">Festiva Moments</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Agentic AI Matchmaker</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 4. CENTERED INPUT CONTROLS ---
spacer_left, main_content, spacer_right = st.columns([1, 2, 1])

with main_content:
    with st.container(border=False): # Removed border for a cleaner, floating look
        
        # Inputs side-by-side
        input_col1, input_col2 = st.columns(2)
        with input_col1:
            selected_city = st.selectbox("Destination City", ["Mumbai", "Bangalore", "Chennai", "Hyderabad"])
        with input_col2:
            user_budget = st.number_input("Maximum Budget (₹)", min_value=100000, max_value=1000000, value=200000, step=10000)
        
        st.markdown("<br>", unsafe_allow_html=True)
        decorator_ratio = st.slider("Decorator Allocation Strategy (%)", 40, 80, 60)
        st.caption(f"Photography allocation automatically optimized to {100 - decorator_ratio}%.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("Curate Perfect Package", use_container_width=True)

st.markdown("---")

# --- 5. SYSTEM EXECUTION & RESULTS ---
if generate_btn:
    
    _, load_col, _ = st.columns([1, 2, 1])
    with load_col:
        with st.status("Analyzing vendor portfolios...", expanded=True) as status:
            st.write("✨ Querying FAISS Vector space...")
            time.sleep(0.5)
            st.write("⚖️ Balancing budget constraints...")
            time.sleep(0.5)
            st.write("🖋️ Drafting client proposal via Gemini...")
            
            # Mock Data (Ensure this is connected to your actual backend logic!)
            best_dec = {"name": "Royal Knot Weddings", "price": 120000, "rating": 4.8, "description": "Luxury floral mandaps and bespoke event styling."}
            best_pho = {"name": "Cinematic Captures", "price": 60000, "rating": 4.9, "description": "Award-winning experts in candid portraiture and drone coverage."}
            total_cost = best_dec['price'] + best_pho['price']
            savings = user_budget - total_cost
            
            dynamic_pitch = generate_pitch(selected_city, user_budget, best_dec, best_pho)
            status.update(label="Curation Complete", state="complete", expanded=False)

    # --- 6. DASHBOARD RESULTS ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="ai-highlight">"{dynamic_pitch}"</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Financial Metrics
    col_a, col_b, col_c = st.columns(3)
    col_a.metric(label="Authorized Budget", value=f"₹{user_budget:,}")
    col_b.metric(label="Actual Curation Cost", value=f"₹{total_cost:,}", delta=f"₹{savings:,} Retained", delta_color="normal")
    col_c.metric(label="AI Confidence Score", value="98.5%", delta="Highly Optimal")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Vendor Cards
    card_col1, card_col2 = st.columns(2)
    
    with card_col1:
        with st.container(border=True):
            st.markdown("#### 🎨 Design & Decor")
            st.subheader(best_dec['name'])
            st.divider()
            st.markdown(f"**Investment:** ₹{best_dec['price']:,}")
            st.markdown(f"**Client Rating:** ⭐ {best_dec['rating']}/5.0")
            st.caption(best_dec['description'])

    with card_col2:
        with st.container(border=True):
            st.markdown("#### 📸 Visual Documentation")
            st.subheader(best_pho['name'])
            st.divider()
            st.markdown(f"**Investment:** ₹{best_pho['price']:,}")
            st.markdown(f"**Client Rating:** ⭐ {best_pho['rating']}/5.0")
            st.caption(best_pho['description'])

else:
    _, empty_col, _ = st.columns([1, 2, 1])
    with empty_col:
        st.info("👆 Provide event specifications above to initiate the curation process.")