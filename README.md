# 💪 FitBuddy

**FitBuddy** is an AI-powered personalized workout planning web application built with **FastAPI, Google Gemini AI, Jinja2, SQLite, and SQLAlchemy**.

The application allows users to enter basic fitness information, generate a personalized 7-day workout plan, and then provide feedback to generate an updated plan.

---

## 📌 Project Overview

FitBuddy helps users create a simple and personalized weekly fitness routine.

The user provides:

- Name
- Age
- Weight
- Fitness goal
- Preferred workout intensity

FitBuddy sends this information to Gemini AI and generates a **7-day workout plan** containing activities, durations, and recovery/safety guidance.

Users can then use the **Update My Plan** feature to provide feedback such as:

> Make Day 3 easier and add more stretching.

FitBuddy uses that feedback to generate an updated plan.

---

## ✨ Features

- 🏋️ Personalized 7-day workout plan generation
- 🤖 Gemini AI integration
- 👤 User profile information
- 🎯 Fitness goal and intensity selection
- 🛡️ Recovery and safety guidance
- 🥗 General nutrition guidance
- 📝 Feedback-based workout plan updates
- 💾 SQLite database storage
- 🗃️ SQLAlchemy ORM
- 🎨 HTML/CSS/Jinja2 interface
- 📋 View All Users page
- 📚 FastAPI Swagger API documentation
- 🔄 Original and updated workout plans
- 🧹 Markdown-to-HTML formatting
- 🐙 Git/GitHub version control

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | Backend web framework |
| Uvicorn | Application server |
| Google Gemini AI | Workout-plan generation |
| Jinja2 | HTML templating |
| HTML | Frontend structure |
| CSS | Frontend styling |
| SQLite | Database |
| SQLAlchemy | Database ORM |
| Python Markdown | Markdown-to-HTML conversion |
| Git | Version control |
| GitHub | Source-code hosting |

---

## 🏗️ Application Architecture

```text
User Browser
     │
     ▼
FastAPI Application
     │
     ├──────────────► Gemini AI
     │                    │
     │                    ▼
     │              Workout Plan
     │
     ├──────────────► SQLAlchemy
     │                    │
     │                    ▼
     │                  SQLite
     │
     ▼
Jinja2 Templates
     │
     ▼
HTML/CSS Result Page
```

---

## 📂 Project Structure

```text
FitBuddy/
│
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── gemini_generator.py
│   ├── models.py
│   └── database.py
│
├── templates/
│   ├── index.html
│   ├── result.html
│   └── all_users.html
│
├── static/
│   └── style.css
│
├── fitbuddy-env/
│
├── .env
├── .gitignore
└── README.md
```

> `fitbuddy-env` is the local Python virtual environment and normally should not be committed to GitHub.

---

## ⚙️ Requirements

Before running FitBuddy, make sure you have:

- Python 3.x
- Git
- A Google Gemini API key
- Internet connection for Gemini API requests

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/barani1004/FitBuddy.git
```

### 2. Open the project folder

```bash
cd FitBuddy
```

### 3. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv fitbuddy-env
```

### 4. Activate the virtual environment

```powershell
.itbuddy-env\Scripts\Activate.ps1
```

You should see:

```text
(fitbuddy-env)
```

in your terminal.

### 5. Install dependencies

If your project has a `requirements.txt` file:

```powershell
pip install -r requirements.txt
```

If dependencies need to be installed individually, install the packages used by the project, including FastAPI, Uvicorn, SQLAlchemy, Jinja2, Python Markdown, python-dotenv, and the Google GenAI SDK.

---

## 🔑 Gemini API Configuration

Create a `.env` file in the project root.

Add your Gemini API key using the environment-variable name expected by `app/gemini_generator.py`.

Example:

```env
GEMINI_API_KEY=your_api_key_here
```

**Do not upload your real API key to GitHub.**

Make sure `.env` is included in `.gitignore`.

---

## ▶️ Running the Application

Activate the virtual environment:

```powershell
.itbuddy-env\Scripts\Activate.ps1
```

Then start the FastAPI server:

```powershell
uvicorn app.main:app --reload
```

The application will normally be available at:

```text
http://127.0.0.1:8000/
```

Open that address in your browser.

---

## 🌐 Important URLs

When the application is running:

| Page | URL |
|---|---|
| 🏠 Home | `http://127.0.0.1:8000/` |
| 👥 View All Users | `http://127.0.0.1:8000/view-all-users` |
| 📚 Swagger API Docs | `http://127.0.0.1:8000/docs` |

---

## 🔄 How FitBuddy Works

### Step 1 — Enter User Information

The user enters:

```text
Name
Age
Weight
Goal
Intensity
```

### Step 2 — Generate Plan

The application sends the information to Gemini AI.

Gemini generates a personalized 7-day workout plan.

### Step 3 — Save Information

The user and generated workout plan are saved in the SQLite database.

### Step 4 — Display Result

The result page displays:

- Personalized greeting
- Age
- Weight
- Goal
- Intensity
- 7-day workout plan
- Recovery/safety guidance
- Nutrition tip

### Step 5 — Give Feedback

The user can enter feedback using:

**Update My Plan**

For example:

```text
Make Day 3 easier and add more stretching.
```

### Step 6 — Generate Updated Plan

FitBuddy sends the feedback together with the user's context to Gemini AI.

Gemini generates an updated 7-day plan.

---

## 🔌 API Endpoints

### `GET /`

Displays the FitBuddy home page.

### `POST /generate`

Generates a new personalized workout plan.

### `POST /submit-feedback`

Generates an updated workout plan based on user feedback.

### `GET /view-all-users`

Displays stored users and workout-plan information.

### `GET /docs`

Opens FastAPI's interactive Swagger documentation.

---

## 🗄️ Database

FitBuddy uses **SQLite** for local data storage.

SQLAlchemy is used as the ORM.

The project stores information about:

### User

- `id`
- `name`
- `age`
- `weight`
- `goal`
- `intensity`

### WorkoutPlan

- `id`
- `user_id`
- `plan`
- `nutrition_tip`

The `user_id` connects a workout plan to its user.

---

## 🧪 Testing

The main application flow was tested locally:

- Home page
- Workout generation
- Result page
- Feedback submission
- Updated workout plan
- User information display
- View All Users
- Swagger API documentation

The feedback workflow was also tested with an example where the user requested an easier Day 3 and additional stretching.

---

## 🐛 Debugging Completed

During development, several issues were identified and fixed:

- Fixed an Internal Server Error caused by missing template result data.
- Fixed `user_id` validation by using the required integer ID.
- Fixed missing Age, Weight, Goal, and Intensity values on the updated result page.
- Fixed Markdown heading formatting.
- Fixed nutrition-tip display handling.
- Tested the complete generate → feedback → update workflow.

---

## 🖥️ One-Click Local Startup

For Windows, a batch launcher can be added to start the application more easily.

Example:

```bat
@echo off
cd /d "%~dp0"

call fitbuddy-env\Scripts\activate.bat

start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:8000/"

uvicorn app.main:app --reload
```

Save it as:

```text
start_fitbuddy.bat
```

Then double-click the file to start the local application and open the home page.

---

## 🔐 Security Notes

- Keep the Gemini API key in an environment variable.
- Never commit `.env` or secret API keys to GitHub.
- The current project is intended primarily for local development/testing.
- A production deployment would require additional security measures such as authentication, stronger secret management, rate limiting, and production database configuration.

---

## 🚀 Future Enhancements

Possible future improvements include:

- User authentication
- Individual user accounts
- Workout completion tracking
- Progress history
- Fitness progress charts
- More detailed nutrition planning
- Cloud deployment
- PostgreSQL or another production database
- Automated tests
- CI/CD pipeline
- Mobile application or PWA

---

## 📌 Current Project Status

**FitBuddy development version is complete and tested locally.**

The latest Git commit is:

```text
273aac9
Complete FitBuddy workout planning and feedback features
```

The completed changes have been pushed to the `main` branch of the GitHub repository.

---

## 👨‍💻 Project

**Repository:**  
https://github.com/barani1004/FitBuddy

**Project:** FitBuddy  
**Type:** AI-powered fitness planning web application  
**Backend:** FastAPI  
**AI:** Google Gemini  
**Database:** SQLite + SQLAlchemy

---

## 📄 License

Add the license required by your institution or project before distributing the application publicly.
