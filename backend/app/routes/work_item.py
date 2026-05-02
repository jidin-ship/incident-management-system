from fastapi import APIRouter
from app.db.postgres import SessionLocal
from app.models.work_item import WorkItem
from datetime import datetime

router = APIRouter()

# Get all work items
@router.get("/work-items")
def get_work_items():
    db = SessionLocal()
    items = db.query(WorkItem).all()
    db.close()

    return items


# Update status
@router.post("/work-items/{item_id}/status")
def update_status(item_id: int, status: str):
    db = SessionLocal()
    item = db.query(WorkItem).filter(WorkItem.id == item_id).first()

    if not item:
        return {"error": "Work item not found"}

    # Prevent closing without RCA
    if status == "CLOSED" and not item.rca:
        return {"error": "Cannot close without RCA"}

    item.status = status

    if status == "RESOLVED":
        item.resolved_at = datetime.utcnow()

    db.commit()
    db.close()

    return {"message": "Status updated"}

@router.post("/work-items/{item_id}/rca")
def add_rca(item_id: int, rca: str):
    db = SessionLocal()
    item = db.query(WorkItem).filter(WorkItem.id == item_id).first()

    if not item:
        return {"error": "Work item not found"}

    item.rca = rca
    db.commit()
    db.close()

    return {"message": "RCA added"}
