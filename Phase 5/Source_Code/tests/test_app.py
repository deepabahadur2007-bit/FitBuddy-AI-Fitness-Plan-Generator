from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_homepage():

    response = client.get("/")

    assert response.status_code == 200

    assert "FitBuddy" in response.text


def test_health():

    response = client.get(
        "/api/health"
    )

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_generate_and_feedback():

    payload = {

        "username": "Test User",

        "user_id": "TEST001",

        "age": 25,

        "weight": 65,

        "goal": "general wellness",

        "intensity": "medium",

    }


    response = client.post(

        "/api/generate-workout",

        json=payload,

    )


    assert response.status_code == 200


    data = response.json()


    assert data["plan_id"]

    assert "DAY 1" in data["workout_plan"]


    feedback = {

        "user_id": "TEST001",

        "feedback":
            "Add more mobility work.",

    }


    response = client.post(

        "/api/submit-feedback",

        json=feedback,

    )


    assert response.status_code == 200


    assert "updated_plan" in response.json()
