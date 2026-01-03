import streamlit as st
from utils.ollama_client import generate_diet_plan

st.title("AI Diet Plan Maker")
st.image("images/image.png", width=100)

age = st.number_input("Age", min_value=10, max_value=100, value=25)
weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
height = st.number_input("Height (cm)", min_value=120.0, max_value=220.0, value=170.0)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
goal = st.text_input("Goal (e.g. weight loss, muscle gain)", "weight loss")
diet_type = st.selectbox("Diet type", ["vegetarian", "vegan", "non-vegetarian"])
activity = st.selectbox("Activity level", ["low", "moderate", "high"])

if st.button("Generate Diet Plan"):
    with st.spinner("Talking to AI, please wait..."):
        try:
            plan = generate_diet_plan(
                age=int(age),
                gender=gender,
                weight_kg=float(weight),
                height_cm=float(height),
                goal=goal,
                diet_type=diet_type,
                activity_level=activity,
            )
            st.markdown(plan)
        except Exception as e:
            st.error(f"Error generating plan: {e}")