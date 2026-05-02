from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.postgres import Base

class WorkItem(Base):
    __tablename__ = "work_items"

    id = Column(Integer, primary_key=True, index=True)
    component_id = Column(String, index=True)
    status = Column(String, default="OPEN")

    created_at = Column(DateTime, default=datetime.utcnow)

    # RCA fields
    rca = Column(String, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
