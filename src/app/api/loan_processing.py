from fastapi import APIRouter
from typing import List
from src.ml_project.entity.config_entity import LoanApplication
from src.ml_project.pipeline.prediction import PredictionPipeline

router = APIRouter()
pipeline = PredictionPipeline()

@router.post("/process_loan_applications")
async def process_loan_applications(applications: List[LoanApplication]):
    # Use prediction pipeline to process logic on the inputs
    results = pipeline.predict(applications)
    
    return {
        "status": "success",
        "processed_count": len(applications),
        "results": results
    }

@router.get("/ping")
async def pong():
    return {"ping": "pong!"}
