import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_workout_gemini(
    name,
    age,
    weight,
    goal,
    intensity
):
    prompt = f"""
Create a personalized 7-day fitness plan.

Name: {name}
Age: {age}
Weight: {weight}
Goal: {goal}
Preferred intensity: {intensity}

For each of the 7 days, provide:
- Workout/activity
- Approximate duration
- A short recovery or safety note


Keep the recommendations appropriate for the person's age and avoid extreme dieting or excessive exercise.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return {
        "name": name,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity,
        "plan": response.text,
        "nutrition_tip": "Follow a balanced diet, stay hydrated, and choose nutritious foods that support your daily activities."
    }

def update_workout_plan(original_plan, feedback):
    prompt = f"""
Update the following fitness plan based on the user's feedback.

Original workout plan:
{original_plan}

User feedback:
{feedback}

Create an updated 7-day workout plan that incorporates the user's feedback.

Keep the plan appropriate for the user's age and avoid extreme dieting,
excessive exercise, or unsafe recommendations.

Return only the updated workout plan.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text