from fastapi import FastAPI
from src.app.api import loan_processing

def create_app() -> FastAPI:
    app = FastAPI(
        title="ML Project FastAPI",
        description="FastAPI service for processing loan applications.",
        version="1.0.0"
    )

    app.include_router(loan_processing.router)
    return app

app = create_app()
