from .config import get_settings
from .gemini_client import generate_text


def _demo_update(
    original_plan: str,
    feedback: str,
) -> str:

    return f"""
UPDATED FITBUDDY PLAN

USER FEEDBACK:

{feedback}


The original plan has been adjusted conceptually
to reflect the requested feedback.

Keep the existing 7-day structure.

Adjust workload gradually.

Preserve appropriate recovery days.


ORIGINAL PLAN:

{original_plan}


Demo mode note:

Configure GEMINI_API_KEY to have Gemini
rewrite the complete personalized plan.
"""


def update_workout_plan(
    original_plan: str,
    feedback: str,
    goal: str,
    intensity: str,
) -> str:

    settings = get_settings()

    prompt = f"""
You are revising an existing 7-day fitness plan.

Fitness goal:
{goal}

Preferred intensity:
{intensity}


ORIGINAL PLAN:

{original_plan}


USER FEEDBACK:

{feedback}


TASK:

Return a complete revised 7-day plan.

Do NOT return only a list of changes.

Respect the user's feedback where reasonable.

Keep useful structure.

Include:

• warm-up
• main workout
• sets/repetitions or duration
• rest guidance
• cooldown/recovery
• appropriate recovery days

Do not provide medical diagnosis or treatment.

Do not provide dangerous exercise recommendations.

Include a short general safety note.
"""

    if settings.gemini_api_key:

        try:

            return generate_text(
                prompt,
                settings.workout_model,
                6000,
            )

        except Exception:

            if not settings.demo_mode:
                raise

    if settings.demo_mode:

        return _demo_update(
            original_plan,
            feedback,
        )

    raise RuntimeError(
        "Gemini is not configured."
    )