import ollama

def get_pose_info(pose_name: str) -> str:
    prompt = f"""
You are a yoga expert. For the asana '{pose_name}', provide:

1. **Key Benefits** (3-5 bullet points, physical/mental)

2. **Step-by-Step Instructions** (3-5 bullet points, beginner-friendly)

3. **Precautions** (1-2 warnings)

Keep response concise, accurate, and safe. Use markdown.
"""
    response = ollama.chat(
        model='phi3:mini',
        messages=[{'role': 'user', 'content': prompt}],
        stream=False
    )
    return response['message']['content']


def generate_diet_plan(
    age: int,
    gender: str,
    weight_kg: float,
    height_cm: float,
    goal: str,
    diet_type: str = "balanced",
    activity_level: str = "moderate"
) -> str:
    """
    Generate a personalized diet plan using a local Ollama model.
    """

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

2. Keep meals realistic for an Indian context when possible, using commonly available foods and are healthy and balanced and provide variety and list of different meals each day.

3. For each meal, give:
   - Description of the dish
   - Very rough calorie estimate (only if confident)
   - For each meal include types of food(eg for lunch include atleast 6-7 different meals)

4. Add a short **Daily Notes** section for each day with:
   - Water intake guideline
   - Simple lifestyle tip.

5. Safety:
   - Do NOT give medical advice or claim to cure diseases.
   - If data is insufficient, add a short disclaimer at the end.

Format the response clearly using markdown headings and bullet points.
"""

    response = ollama.chat(
        model='phi3:mini',
        messages=[{'role': 'user', 'content': prompt}],
        stream=False
    )
    return response['message']['content']
