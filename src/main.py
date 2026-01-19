from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.app.core.config import settings
from src.app.api.endpoints import events, calendar

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (e.g., DB connection check, Redis pool)
    print("Startup: CTF Tracker is initializing...")
    yield
    # Shutdown logic
    print("Shutdown: Cleanup resources...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Include Routers
app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(calendar.router, prefix="/calendar", tags=["calendar"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}

@app.get("/")
async def root():
    return {
        "message": "Welcome to the CTF & Conference Tracker API",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
