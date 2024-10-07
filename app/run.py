import uvicorn

from app.main import app
from core.config import settings

if __name__ == "__main__":
    if settings.RUNNING_MODE == "uvicorn":
        # uvicorn.run(app="app.main:app", host=settings.LISTENING_HOST, port=settings.LISTENING_PORT, reload=True)
        uvicorn.run(app="app.main:app", host="localhost", port=8000, reload=True)