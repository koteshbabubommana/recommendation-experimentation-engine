import json
import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

from app.api.schemas import RecommendationRequest, ExperimentRequest, EventRequest
from app.database.connection import get_db
from app.database.models import RecommendationLog, ExperimentEvent
from app.recommendation.recommendation_service import generate_recommendations
from app.experimentation.experiment_service import get_experiment_assignment
from app.analytics.metrics_service import summarize_recommendations, summarize_events
from app.cache.redis_client import cache
from app.streaming.kafka_producer import event_producer
from app.monitoring.prometheus_metrics import (
    recommendation_requests_total,
    experiment_assignments_total,
    recommendation_latency_seconds
)
from app.workers.event_processor import process_event_async

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "recommendation-experimentation-engine"
    }


@router.post("/recommendations")
async def recommendations(request: RecommendationRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    recommendation_requests_total.inc()

    cache_key = f"recommendations:{request.user_id}:{request.session_id}"
    cached_result = cache.get(cache_key)

    if cached_result:
        cached_result["cached"] = True
        return cached_result

    result = generate_recommendations(
        user_id=request.user_id,
        candidate_items=request.candidate_items,
        user_features=request.user_features,
        experiment_name=request.experiment_name
    )

    log = RecommendationLog(
        user_id=request.user_id,
        session_id=request.session_id,
        experiment_name=request.experiment_name,
        experiment_group=result["experiment_group"],
        recommended_items=json.dumps(result["recommendations"]),
        top_score=result["top_score"],
        cached=False
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    event_payload = {
        "event_type": "recommendation_generated",
        "user_id": request.user_id,
        "session_id": request.session_id,
        "experiment_group": result["experiment_group"],
        "recommendation_count": len(result["recommendations"])
    }

    event_logged = event_producer.publish_event("recommendation-events", event_payload)
    await process_event_async(event_payload)

    response = {
        "request_id": log.id,
        "user_id": request.user_id,
        "experiment_group": result["experiment_group"],
        "recommendations": result["recommendations"],
        "cached": False,
        "event_logged": event_logged,
        "latency_ms": round((time.time() - start_time) * 1000, 2)
    }

    cache.set(cache_key, response)
    recommendation_latency_seconds.observe(time.time() - start_time)

    return response


@router.post("/experiment/assign")
async def assign_experiment(request: ExperimentRequest):
    experiment_assignments_total.inc()

    return get_experiment_assignment(
        user_id=request.user_id,
        experiment_name=request.experiment_name
    )


@router.post("/events")
async def track_event(request: EventRequest, db: Session = Depends(get_db)):
    assignment = get_experiment_assignment(
        user_id=request.user_id,
        experiment_name=request.metadata.get("experiment_name", "homepage-ranking-test")
    )

    event = ExperimentEvent(
        user_id=request.user_id,
        experiment_name=assignment["experiment_name"],
        experiment_group=assignment["experiment_group"],
        event_type=request.event_type,
        item_id=request.item_id
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    event_payload = {
        "event_id": event.id,
        "user_id": request.user_id,
        "event_type": request.event_type,
        "item_id": request.item_id,
        "experiment_group": assignment["experiment_group"]
    }

    event_logged = event_producer.publish_event("experiment-events", event_payload)
    await process_event_async(event_payload)

    return {
        "event_id": event.id,
        "stored": True,
        "event_logged": event_logged
    }


@router.get("/analytics/recommendations")
async def recommendation_analytics(db: Session = Depends(get_db)):
    logs = db.query(RecommendationLog).all()
    return summarize_recommendations(logs)


@router.get("/analytics/events")
async def event_analytics(db: Session = Depends(get_db)):
    events = db.query(ExperimentEvent).all()
    return summarize_events(events)


@router.get("/recommendation-history")
async def recommendation_history(db: Session = Depends(get_db)):
    logs = db.query(RecommendationLog).order_by(RecommendationLog.id.desc()).limit(10).all()

    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "experiment_name": log.experiment_name,
            "experiment_group": log.experiment_group,
            "top_score": log.top_score,
            "cached": log.cached,
            "created_at": log.created_at
        }
        for log in logs
    ]


@router.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)