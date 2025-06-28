from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.api.v1.endpoints import router as v1_router
from app.configs.config import get_config
from app.utils.logger import Loggers, log

config = get_config()

# Loggers.init_config(log_level=config.app.log_level) # Initialize logging configuration(If needed)

app = FastAPI(
    title=config.app.name,
    description=config.app.description,
    version=config.app.version,
)

app.include_router(v1_router, prefix="/api/v1", tags=["llm-analysis"])


@app.get("/health")
def health_check() -> dict:
    """
    Health check endpoint.

    Returns:
        dict: Service health status.
    """
    log.info({"event": "health_check"})
    return {"status": "ok"}
