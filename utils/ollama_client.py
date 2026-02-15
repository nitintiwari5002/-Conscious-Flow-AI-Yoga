import requests
import streamlit as st

api_key = st.secrets["key"]

GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "qwen/qwen3-32b"  # Qwen 3 32B model id[web:17]


def _groq_chat(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",  # Bearer auth header[web:14]
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 0.7,
    }

    resp = requests.post(GROQ_BASE_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    return data["choices"][0]["message"]["content"]


def get_pose_info(pose: str) -> str:
    prompt = f"""
You are a yoga expert. For the asana '{pose}', provide faster results for the following:

1. **Key Benefits** (3-4 bullet points, physical/mental)

2. **Step-by-Step Instructions** (3-4 bullet points, beginner-friendly)

3. **Related Asanas** (3-4 suggestions)

Keep response concise and accurate.
"""
    return _groq_chat(prompt)


def generate_diet_plan(
    age: int,
    gender: str,
    weight_kg: float,
    height_cm: float,
    goal: str,
    diet_type: str = "balanced",
    activity_level: str = "moderate",
) -> str:
    prompt = f"""
You are a certified nutritionist and diet planner and your task is to create a detailed diet plan that could be repeated and that is healthy.

Create a personalized healthy plan with the following details:

Person:
- Age: {age} years
- Gender: {gender}
- Weight: {weight_kg} kg
- Height: {height_cm} cm
- Activity level: {activity_level}
- Goal: {goal} (e.g., weight loss, muscle gain, maintenance)
- Preferred diet style: {diet_type} (e.g., vegetarian, vegan, non-vegetarian, balanced)

Instructions:
1. For each day, list:
   - Breakfast
   - Lunch
   - Evening snack
   - Dinner

2. Keep meals realistic for an Indian context when possible, using commonly available foods and are healthy and balanced and provide variety and list of different meals.

3. For each meal, give:
   - Description of the dish
   - Very rough calorie estimate (only if confident)
   - For each meal include types of food (eg for lunch include at least 6-7 different meals)

4. Add a short **Daily Notes** section for each day with:
   - Water intake guideline
   - Simple lifestyle tip.

5. Safety:
   - Do NOT give medical advice or claim to cure diseases.
   - If data is insufficient, add a short disclaimer at the end.

Format the response clearly using markdown headings and bullet points.
"""
    return _groq_chat(prompt)
