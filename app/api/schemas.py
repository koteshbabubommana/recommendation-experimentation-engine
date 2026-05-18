from pydantic import BaseModel
from typing import List, Optional


class RecommendationRequest(BaseModel):
    user_id: str
    session_id: str
    candidate_items: List[str]
    user_features: dict
    experiment_name: Optional[str] = "homepage-ranking-test"


class RecommendationResponse(BaseModel):
    user_id: str
    experiment_group: str
    recommendations: list
    cached: bool
    event_logged: bool


class ExperimentRequest(BaseModel):
    user_id: str
    experiment_name: str = "homepage-ranking-test"


class EventRequest(BaseModel):
    user_id: str
    event_type: str
    item_id: str
    metadata: Optional[dict] = {}