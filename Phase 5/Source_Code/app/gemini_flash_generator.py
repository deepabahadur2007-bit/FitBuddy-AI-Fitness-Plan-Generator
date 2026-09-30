from .config import get_settings
from .gemini_client import generate_text


def _demo_tip(goal: str) -> str:

    tips = {

        "weight loss":
            "Prioritize balanced meals, protein and fiber, "
            "and regular hydration. Avoid aggressive calorie restriction.",

        "muscle gain":
            "Include a protein-rich food in each main meal "
            "and support training with adequate overall calories, "
            "sleep, and hydration.",

        "general wellness":
            "Build meals around vegetables or fruit, a protein source, "
            "whole-food carbohydrates, and adequate fluids.",

        "flexibility":
            "Hydrate well and pair mobility work with balanced meals "
            "and enough protein to support recovery.",
    }

    return tips.get(
        goal,
        "Prioritize balanced nutrition, hydration, recovery, "
        "and consistent sleep.",
    )


def generate_nutrition_tip_with_flash(
    goal: str,
) -> str:

    settings = get_settings()

    prompt = f"""
Give one concise, practical nutrition or recovery tip
for a fitness user whose goal is:

{goal}

Keep it to 2–4 sentences.

Focus on sustainable nutrition, hydration,
sleep, or recovery.

Avoid disease treatment, extreme diets,
or individualized medical claims.
"""

    if settings.gemini_api_key:

        try:

            return generate_text(
                prompt,
                settings.nutrition_model,
                500,
            )

        except Exception:

            if not settings.demo_mode:
                raise

    if settings.demo_mode:

        return _demo_tip(goal)

    raise RuntimeError(
        "Gemini is not configured."
    )