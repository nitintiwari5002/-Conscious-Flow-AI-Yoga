import streamlit as st
from utils.ollama_client import generate_diet_plan

# ---------- Custom CSS ----------
st.markdown(
    """
    <style>
    /* Page background and font */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #020617 60%, #0f766e 100%);
        color: #e5e7eb;
        font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Center main content */
    .main > div {
        max-width: 800px;
        margin: 0 auto;
        padding-top: 1rem;
    }

    /* Title styling */
    .diet-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        color: #fbbf24;
        text-shadow: 0 0 18px rgba(251,191,36,0.45);
    }

    .diet-subtitle {
        text-align: center;
        font-size: 0.95rem;
        color: #cbd5f5;
        margin-bottom: 1.5rem;
    }

    /* Card for form */
    .diet-card {
        background: rgba(15,23,42,0.92);
        border-radius: 18px;
        padding: 1.2rem 1.4rem 1.4rem 1.4rem;
        box-shadow: 0 18px 45px rgba(0,0,0,0.6);
        border: 1px solid rgba(148,163,184,0.35);
        backdrop-filter: blur(16px);
    }

    .diet-section-title {
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
        color: #e5e7eb;
    }

    .diet-section-caption {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-bottom: 0.8rem;
    }

    /* Tweak default Streamlit widgets */
    div[data-baseweb="input"] input,
    div[data-baseweb="select"] select {
        background-color: #020617 !important;
        color: #e5e7eb !important;
    }

    .stButton>button {
        width: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #22c55e, #16a34a);
        color: #0b1120;
        border: none;
        font-weight: 600;
        padding: 0.6rem 0;
        box-shadow: 0 12px 25px rgba(34,197,94,0.4);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #4ade80, #22c55e);
    }

    .diet-output {
        margin-top: 1.5rem;
        padding: 1.2rem 1.4rem;
        border-radius: 14px;
        background: rgba(15,23,42,0.9);
        border: 1px solid rgba(148,163,184,0.4);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("images/image.png", width=70)
with col_title:
    st.markdown('<div class="diet-title">AI Diet Plan Maker</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="diet-subtitle">Personalised diet plan generated using AI – designed for your body, goal and lifestyle.</div>',
        unsafe_allow_html=True,
    )

# ---------- Form Card ----------
st.markdown('<div class="diet-card">', unsafe_allow_html=True)
st.markdown('<div class="diet-section-title">Your details</div>', unsafe_allow_html=True)
st.markdown('<div class="diet-section-caption">Fill these in to generate a customised diet plan.</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
with col2:
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
with col3:
    height = st.number_input("Height (cm)", min_value=120.0, max_value=220.0, value=170.0)

col4, col5 = st.columns(2)
with col4:
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
with col5:
    activity = st.selectbox("Activity level", ["low", "moderate", "high"])

goal = st.text_input("Goal (e.g. weight loss, muscle gain)", "weight loss")
diet_type = st.selectbox("Diet type", ["vegetarian", "vegan", "non-vegetarian"])

generate_clicked = st.button("Generate Diet Plan")

st.markdown("</div>", unsafe_allow_html=True)  # close diet-card

# ---------- Output ----------
if generate_clicked:
    with st.spinner("Talking to AI, please wait..."):
        try:
            plan = generate_diet_plan(
                age=int(age),
                gender=gender,
                weight_kg=float(weight),
                height_cm=float(height),
                goal=goal,
                diet_type=diet_type,
                activity_level=activity
            )
            st.markdown('<div class="diet-output">', unsafe_allow_html=True)
            st.markdown(plan)
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error generating plan: {e}")
