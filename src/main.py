from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

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

# Mount Static Files
static_dir = os.path.join(os.path.dirname(__file__), "app/static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root():
    return FileResponse(os.path.join(static_dir, "index.html"))


@app.get("/health")
async def health_check():
    from src.app.services.health import check_health_status

    status = await check_health_status()
    if status["overall"] != "PASS":
        # In a real K8s probe we might return 500, but for now 200 with details is fine
        pass
    return status


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)  # nosec
