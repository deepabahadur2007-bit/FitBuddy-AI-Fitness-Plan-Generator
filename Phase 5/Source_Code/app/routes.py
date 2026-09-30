from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic import ValidationError

from sqlalchemy.orm import Session

from .config import get_settings

from .crud import (
    get_all_users,
    get_latest_plan,
    get_user,
    save_plan,
    save_user,
    update_plan,
)

from .database import get_db

from .gemini_flash_generator import (
    generate_nutrition_tip_with_flash,
)

from .gemini_generator import (
    generate_workout_gemini,
)

from .schemas import (
    FeedbackRequest,
    UserInput,
)

from .updated_plan import (
    update_workout_plan,
)


router = APIRouter()


templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent / "templates"
)


def render_error(
    request: Request,
    message: str,
    status_code: int = 400,
):

    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "message": message
        },
        status_code=status_code,
    )


# ============================================================
# HOME
# ============================================================

@router.get(
    "/",
    response_class=HTMLResponse,
)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "FitBuddy"
        },
    )


# ============================================================
# GENERATE WORKOUT
# ============================================================

@router.post(
    "/generate-workout",
    response_class=HTMLResponse,
)
def generate_workout(

    request: Request,

    username: str = Form(...),

    user_id: str = Form(...),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...),

    db: Session = Depends(get_db),

):

    try:

        data = UserInput(

            username=username,

            user_id=user_id,

            age=age,

            weight=weight,

            goal=goal,

            intensity=intensity,

        )

    except ValidationError as exc:

        return render_error(
            request,
            str(exc),
            422,
        )

    try:

        user = save_user(
            db,
            data,
        )

        workout = generate_workout_gemini(

            data.username,

            data.age,

            data.weight,

            data.goal,

            data.intensity,

        )

        nutrition_tip = (
            generate_nutrition_tip_with_flash(
                data.goal
            )
        )

        plan = save_plan(

            db,

            user,

            workout,

            nutrition_tip,

        )

    except Exception as exc:

        return render_error(
            request,
            f"Could not generate the plan: {exc}",
            502,
        )

    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context={

            "user": user,

            "plan": plan,

            "current_plan": plan.original_plan,

            "is_updated": False,

        },

    )


# ============================================================
# FEEDBACK
# ============================================================

@router.post(
    "/submit-feedback",
    response_class=HTMLResponse,
)
def submit_feedback(

    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...),

    db: Session = Depends(get_db),

):

    try:

        data = FeedbackRequest(

            user_id=user_id,

            feedback=feedback,

        )

    except ValidationError as exc:

        return render_error(
            request,
            str(exc),
            422,
        )

    user = get_user(
        db,
        data.user_id,
    )

    if not user:

        return render_error(
            request,
            "User ID was not found.",
            404,
        )

    plan = get_latest_plan(
        db,
        user,
    )

    if not plan:

        return render_error(
            request,
            "No workout plan exists for this user.",
            404,
        )

    base_plan = (
        plan.updated_plan
        or plan.original_plan
    )

    try:

        revised = update_workout_plan(

            base_plan,

            data.feedback,

            user.goal,

            user.intensity,

        )

        update_plan(

            db,

            plan,

            revised,

            data.feedback,

        )

        plan.nutrition_tip = (
            generate_nutrition_tip_with_flash(
                user.goal
            )
        )

        db.commit()

        db.refresh(plan)

    except Exception as exc:

        return render_error(
            request,
            f"Could not update the plan: {exc}",
            502,
        )

    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context={

            "user": user,

            "plan": plan,

            "current_plan": plan.updated_plan,

            "is_updated": True,

        },

    )


# ============================================================
# ADMIN / COACH DASHBOARD
# ============================================================

@router.get(
    "/view-all-users",
    response_class=HTMLResponse,
)
def view_all_users(

    request: Request,

    db: Session = Depends(get_db),

):

    users = get_all_users(db)

    return templates.TemplateResponse(

        request=request,

        name="all_users.html",

        context={
            "users": users
        },

    )


# ============================================================
# HEALTH API
# ============================================================

@router.get("/api/health")
def health():

    settings = get_settings()

    return {

        "status": "ok",

        "service": "FitBuddy",

        "gemini_configured":
            bool(settings.gemini_api_key),

        "demo_mode":
            settings.demo_mode,

    }


# ============================================================
# API - GENERATE WORKOUT
# ============================================================

@router.post("/api/generate-workout")
def api_generate_workout(

    data: UserInput,

    db: Session = Depends(get_db),

):

    try:

        user = save_user(
            db,
            data,
        )

        workout = generate_workout_gemini(

            data.username,

            data.age,

            data.weight,

            data.goal,

            data.intensity,

        )

        nutrition_tip = (
            generate_nutrition_tip_with_flash(
                data.goal
            )
        )

        plan = save_plan(

            db,

            user,

            workout,

            nutrition_tip,

        )

        return {

            "user_id":
                user.user_id,

            "plan_id":
                plan.id,

            "workout_plan":
                workout,

            "nutrition_tip":
                nutrition_tip,

        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )


# ============================================================
# API - FEEDBACK
# ============================================================

@router.post("/api/submit-feedback")
def api_submit_feedback(

    data: FeedbackRequest,

    db: Session = Depends(get_db),

):

    user = get_user(
        db,
        data.user_id,
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User ID was not found.",
        )

    plan = get_latest_plan(
        db,
        user,
    )

    if not plan:

        raise HTTPException(
            status_code=404,
            detail="No workout plan exists for this user.",
        )

    base_plan = (
        plan.updated_plan
        or plan.original_plan
    )

    try:

        revised = update_workout_plan(

            base_plan,

            data.feedback,

            user.goal,

            user.intensity,

        )

        update_plan(

            db,

            plan,

            revised,

            data.feedback,

        )

        return {

            "user_id":
                user.user_id,

            "plan_id":
                plan.id,

            "updated_plan":
                revised,

            "feedback":
                data.feedback,

        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )