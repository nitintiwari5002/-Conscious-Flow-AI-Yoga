import requests
import streamlit as st

# Fixed secrets key for Streamlit Cloud
api_key = st.secrets["groq_key"]  # Set in .streamlit/secrets.toml or Cloud settings

GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "qwen/qwen3-32b"  # Your Qwen3 model

def _groq_chat(prompt: str) -> str:
    """Core chat function - NO THINKING enabled."""
    # Disable thinking completely
    no_think_prompt = f"""/no_think
/no reasoning
Direct, concise answer only. No explanations, steps, or <think> tags.

/prompt/
{prompt}"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": no_think_prompt}],
        "temperature": 0.1,  # Consistent, direct responses
        "top_p": 0.8,
        "stream": False,
        "max_tokens": 1500,  # Limit for diet plans
    }
    
    try:
        resp = requests.post(GROQ_BASE_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()
        
        # Strip any remaining think tags (failsafe)
        content = content.replace("<think>", "").replace("</think>", "").replace("**Think**", "").strip()
        return content
    except requests.exceptions.RequestException as e:
        return f"API Error (check key/internet): {str(e)[:100]}"
    except (KeyError, IndexError) as e:
        return f"Response Error: {str(e)}"

def get_pose_info(pose: str) -> str:
    """Get detailed info for a specific pose."""
    prompt = f"""Yoga expert: For '{pose}' provide ONLY:

1. **Key Benefits** (3-4 bullets)
2. **Steps** (3-4 numbered steps, beginner)
3. **Duration**: 30-60s hold

Concise, accurate."""
    return _groq_chat(prompt)

def pose_predictor(condition: str) -> str:
    """Recommend poses for user condition/problem."""
    prompt = f"""Yoga therapist: For condition '{condition}' recommend 2-3 beginner poses.

Format:
**Pose 1**: Benefits. Steps: 1.2.3.
**Pose 2**: ...

Safe, effective only."""
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
    """Generate 3-day repeatable diet plan."""
    prompt = f"""Certified nutritionist: Create 3-day Indian-style diet plan for:
Age: {age}, {gender}, {weight_kg}kg, {height_cm}cm
Goal: {goal}, Diet: {diet_type}, Activity: {activity_level}

Per day (Breakfast/Lunch/Snack/Dinner):
- Dish + rough calories
Variety, healthy, realistic foods.

End with Daily Notes (water, tip).
Markdown. No medical claims."""
    return _groq_chat(prompt)
