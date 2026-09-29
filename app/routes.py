from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
import markdown

from .database import SessionLocal
from .models import User, WorkoutPlan
from .gemini_generator import generate_workout_gemini, update_workout_plan
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
        result["user_id"] = user.id

        workout = WorkoutPlan(
            user_id=user.id,
            plan=result["plan"],
            nutrition_tip=result["nutrition_tip"]
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

@router.post("/submit-feedback")
def submit_feedback(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...)
):
    db = SessionLocal()

    try:
        workout = (
            db.query(WorkoutPlan)
            .filter(WorkoutPlan.user_id == user_id)
            .order_by(WorkoutPlan.id.desc())
            .first()
        )
        user = db.query(User).filter(User.id == user_id).first()

        if not workout:
            return templates.TemplateResponse(
                request=request,
                name="result.html",
                context={
                    "request": request,
                    "error": "User or workout plan not found."
                }
            )

        updated_plan = update_workout_plan(
            original_plan=workout.plan,
            feedback=feedback
        )

        workout.updated_plan = updated_plan
        db.commit()

        plan_text = updated_plan

        import re

        plan_text = plan_text.replace("\\\\*", "*")

        plan_text = re.sub(
            r'^\s*\**\s*(Day\s+\d+:[^*]+)\**',
            r'### \1',
            plan_text,
            flags=re.MULTILINE
        )

        plan_html = markdown.markdown(
            plan_text,
            extensions=["extra"]
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "result": {
                    "name": user.name,
                    "age": user.age,
                    "weight": user.weight,
                    "goal": user.goal,
                    "intensity": user.intensity,
                    "user_id": user_id,
                    "nutrition_tip": workout.nutrition_tip or "Follow a balanced diet, stay hydrated, and choose nutritious foods that support your daily activities.",
                },
                "plan_html": plan_html,
                "updated": True
            }
        )

    finally:
        db.close()

@router.get("/view-all-users")
def view_all_users(request: Request):
    db = SessionLocal()

    try:
        users = db.query(User).all()

        user_data = []

        for user in users:
            workout = (
                db.query(WorkoutPlan)
                .filter(WorkoutPlan.user_id == user.id)
                .order_by(WorkoutPlan.id.desc())
                .first()
            )

            original_plan_html = None
            updated_plan_html = None

            if workout:
                original_plan_html = markdown.markdown(
                    workout.plan,
                    extensions=["extra"]
                )

                if workout.updated_plan:
                    updated_plan_html = markdown.markdown(
                        workout.updated_plan,
                        extensions=["extra"]
                    )

            user_data.append({
                "user": user,
                "workout": workout,
                "original_plan_html": original_plan_html,
                "updated_plan_html": updated_plan_html
            })

        return templates.TemplateResponse(
            request=request,
            name="all_users.html",
            context={
                "request": request,
                "user_data": user_data
            }
        )

    finally:
        db.close()