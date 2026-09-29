from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
import markdown

from .database import SessionLocal
from .models import User, WorkoutPlan
from .gemini_generator import generate_workout_gemini

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@router.post("/generate")
def generate_plan(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    weight: str = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    result = generate_workout_gemini(
        name=name,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    db = SessionLocal()

    try:
        user = User(
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        workout = WorkoutPlan(
            user_id=user.id,
            plan=result["plan"],
            nutrition_tip=""
        )

        db.add(workout)
        db.commit()

    finally:
        db.close()

    import re

    plan_text = result["plan"]

    # Remove escaped Markdown characters returned by Gemini.
    plan_text = plan_text.replace("\\*", "*")

    # Convert "Day 1", "Day 2", etc. into proper headings.
    # This prevents the Day headings from becoming bullet points.
    plan_text = re.sub(
        r'^\s*\*\s+\*\*(Day\s+\d+:[^*]+)\*\*',
        r'### \1',
        plan_text,
        flags=re.MULTILINE
    )

    # Convert the remaining Markdown into HTML.
    plan_html = markdown.markdown(
        plan_text,
        extensions=["extra"]
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "result": result,
            "plan_html": plan_html
        }
    )