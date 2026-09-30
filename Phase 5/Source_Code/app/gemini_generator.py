from .config import get_settings
from .gemini_client import generate_text


def _demo_plan(
    username: str,
    goal: str,
    intensity: str,
    age: int,
    weight: float,
) -> str:

    return f"""
FITBUDDY 7-DAY WORKOUT PLAN

Name: {username}
Goal: {goal.title()}
Intensity: {intensity.title()}
Age: {age}
Weight: {weight:g} kg


DAY 1 – FULL BODY FOUNDATION

Warm-up:
7 minutes brisk walking and mobility.

Main Workout:
• Squats – 3 sets × 10 reps
• Incline push-ups – 3 sets × 10 reps
• Rows – 3 sets × 12 reps
• Glute bridges – 3 sets × 12 reps

Cooldown:
5 minutes of easy stretching.


DAY 2 – CARDIO & CORE

Warm-up:
5 minutes easy movement.

Main Workout:
• Moderate cardio – 20–30 minutes
• Plank – 3 × 20–40 seconds
• Dead bug – 3 × 10 each side

Cooldown:
5 minutes walking and stretching.


DAY 3 – RECOVERY & MOBILITY

• Easy walk – 20 minutes
• Gentle mobility – 15 minutes
• Keep the effort comfortable.


DAY 4 – UPPER BODY

Warm-up:
7 minutes.

Main Workout:
• Push-ups – 3 × 8–12
• Rows – 3 × 10–12
• Shoulder press – 3 × 10
• Biceps curls – 2 × 12

Cooldown:
5 minutes.


DAY 5 – LOWER BODY

Warm-up:
7 minutes.

Main Workout:
• Squats – 3 × 10
• Reverse lunges – 3 × 8 each side
• Hip hinge – 3 × 10
• Calf raises – 3 × 15

Cooldown:
5–8 minutes.


DAY 6 – GOAL-FOCUSED CONDITIONING

Warm-up:
5–7 minutes.

Main Workout:
25 minutes of appropriate cardio or conditioning.

Additional:
10 minutes core or mobility work.

Cooldown:
5 minutes.


DAY 7 – REST & RECOVERY

• Rest
• Gentle walking if desired
• Hydration
• Light stretching


PROGRESSION

Increase workload gradually.
Keep approximately 1–3 repetitions in reserve.


SAFETY

Stop if you experience sharp pain, dizziness,
chest pain, or unusual shortness of breath.

This is demo content because Gemini is not configured.
"""


def generate_workout_gemini(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:

    settings = get_settings()

    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Create a practical personalized 7-day workout plan.

USER INFORMATION

Name: {username}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Preferred Intensity: {intensity}


REQUIREMENTS

Create Day 1 through Day 7.

For training days include:

1. Warm-up
2. Main workout
3. Exercises
4. Sets and repetitions or duration
5. Rest guidance
6. Cooldown or recovery

Include appropriate recovery/rest days.

Tailor the plan to:

• fitness goal
• requested intensity
• user's basic profile

Keep the response clear and easy to follow.

Do not diagnose medical conditions.

Do not prescribe medical treatment.

Do not recommend dangerous or extreme exercise.

Include a short safety note.

Return the complete plan in plain text.
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

        return _demo_plan(
            username,
            goal,
            intensity,
            age,
            weight,
        )

    raise RuntimeError(
        "Gemini is not configured."
    )