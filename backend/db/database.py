import os
from sqlalchemy import create_engine, Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:devpass@localhost:5432/copilot")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    log_text = Column(Text)
    cause = Column(Text)
    fix = Column(Text)
    severity = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_incident(log_text: str, cause: str, fix: str, severity: str):
    db = SessionLocal()
    try:
        incident = Incident(
            log_text=log_text,
            cause=cause,
            fix=fix,
            severity=severity
        )
        db.add(incident)
        db.commit()
    finally:
        db.close()

def get_recent_incidents(limit: int = 20):
    db = SessionLocal()
    try:
        return db.query(Incident).order_by(
            Incident.created_at.desc()
        ).limit(limit).all()
    finally:
        db.close()