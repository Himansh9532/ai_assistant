# AI Data Analyst Assessment

This repository contains a FastAPI application with a frontend for candidate registration, exam delivery, and result display.

## Features

- FastAPI backend
- Jinja2 templates and static frontend
- SQLite database for easy deployment
- AI/email services included in backend

## Run locally

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

2. Start the app:

```powershell
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Open in browser:

```
http://localhost:8000
```

## Free deployment options

### Option 1: Deploy with Render (recommended)

Render offers a free static web service and a free web service for small apps.

1. Create a Render account.
2. Connect your GitHub repository.
3. Create a new `Web Service`.
4. Use the following settings:

- Environment: `Docker`
- Dockerfile path: `Dockerfile`
- Build command: leave empty when using Docker
- Start command: leave empty when using Docker
- Plan: `Free`

Render will build and deploy the app using the repository Dockerfile.

### Option 2: Deploy with Railway

Railway can deploy Python services for free with limited resources.

1. Create a Railway account.
2. Create a new project and connect GitHub.
3. Select this repository.
4. Use the `backend` directory as the root.
5. Set build command:

```bash
pip install -r backend/requirements.txt
```

6. Set start command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

7. Deploy.

### Option 3: Deploy with Docker locally or any free Docker host

Build and run with Docker:

```powershell
docker build -t ai-data-analyst-assessment .
docker run -p 8000:8000 ai-data-analyst-assessment
```

Then open:

```
http://localhost:8000
```

## Notes

- The app uses `sqlite:///./assessment.db` by default.
- No extra database setup is required for deployment.
- If your deployment platform provides a `PORT`, use it in the `uvicorn` command.

## GitHub Repository

https://github.com/Himansh9532/ai_assistant
