"""Discovery routes — prospect self-service recommendation."""

from fastapi import APIRouter, HTTPException

from app.models.schemas import DiscoverySession, RecommendationResponse
from app.services.recommendation import generate_recommendation

router = APIRouter(prefix="/api/discovery", tags=["discovery"])


@router.post("/recommend", response_model=RecommendationResponse)
def recommend(session: DiscoverySession) -> RecommendationResponse:
    """
    Accept a discovery session payload and return a deterministic
    service recommendation.
    """
    try:
        return generate_recommendation(session)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {exc}") from exc
