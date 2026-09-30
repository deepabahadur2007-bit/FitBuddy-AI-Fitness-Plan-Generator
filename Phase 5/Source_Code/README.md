# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI + Jinja2 + SQLite application.

It provides:

- Personalized 7-day workout plans
- Nutrition/recovery tips
- Feedback-based plan updates
- SQLite database storage
- Admin/coach dashboard
- REST API
- Swagger API documentation
- Gemini AI integration
- Demo mode for testing without Gemini

---

# Project Structure

```text
FitBuddy/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── gemini_client.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   ├── updated_plan.py
│   ├── routes.py
│   │
│   ├── templates/
│   │   ├── index.html
│   │   ├── result.html
│   │   ├── all_users.html
│   │   └── error.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── images/
│
├── tests/
│   └── test_app.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md