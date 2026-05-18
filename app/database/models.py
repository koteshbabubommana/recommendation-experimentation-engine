from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class RecommendationLog(Base):
    __tablename__ = "recommendation_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    session_id = Column(String)
    experiment_name = Column(String)
    experiment_group = Column(String)
    recommended_items = Column(Text)
    top_score = Column(Float)
    cached = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ExperimentEvent(Base):
    __tablename__ = "experiment_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    experiment_name = Column(String)
    experiment_group = Column(String)
    event_type = Column(String)
    item_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)