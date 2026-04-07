"""Beacon -- Privacy-First AI Protection for Vulnerable Communities.

Powered by Gemma 4 running locally via Ollama. No data ever leaves your device.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from backend.routers import scanner, contracts, rights
from backend.ollama_client import check_model

app = FastAPI(
    title="Beacon",
    description="Privacy-first AI scam protection for vulnerable communities",
    version="1.0.0",
)

# Mount frontend static files
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")
app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")

# Register API routers
app.include_router(scanner.router)
app.include_router(contracts.router)
app.include_router(rights.router)


@app.get("/")
async def serve_index():
    """Serve the main application page."""
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    model_status = await check_model()
    return {
        "status": "ok" if model_status["gemma4_ready"] else "degraded",
        "beacon_version": "1.0.0",
        "model_status": model_status,
    }
