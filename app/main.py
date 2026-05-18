from fastapi import FastAPI
from app.api.routes import router
from app.database.connection import engine
from app.database.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Recommendation Experimentation Engine",
    version="1.0.0",
    description="Real-time recommendation and experimentation engine supporting ranking workflows, feature processing, A/B testing simulation, Redis caching, Kafka event streaming, and analytics pipelines."
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Recommendation Experimentation Engine is running",
        "status": "active"
    }