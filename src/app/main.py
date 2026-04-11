from fastapi import FastAPI
from mangum import Mangum
from src.app.api import loan_processing

from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    app = FastAPI(
        title="ML Project FastAPI",
        description="FastAPI service for processing loan applications.",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(loan_processing.router)

    @app.get("/")
    async def root():
        return {
            "message": "ML Project FastAPI is running!",
            "endpoints": {
                "predict": "/process_loan_applications",
                "health": "/ping"
            }
        }
    return app

app = create_app()
handler = Mangum(app)
