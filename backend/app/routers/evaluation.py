from fastapi import APIRouter
from app.schemas.models import EvaluationRunResponse
from app.services.evaluation_service import evaluation_service

router = APIRouter(prefix="/api/evaluation", tags=["Evaluation"])

@router.post("/run", response_model=EvaluationRunResponse)
async def run_evaluation():
    """
    Executes the 36 ground-truth test cases across Hindi, Kannada, Tamil and RAG groundedness.
    """
    res = evaluation_service.run_all()
    return EvaluationRunResponse(**res)

@router.get("/results")
async def get_fixtures():
    """
    Returns the test case inventory without running inference.
    """
    return {
        "total_test_cases": len(evaluation_service.test_cases),
        "test_cases": evaluation_service.test_cases
    }
