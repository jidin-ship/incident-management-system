from fastapi import APIRouter
from app.db.mongo import signals_collection
from app.db.redis_client import redis_client
from app.db.postgres import SessionLocal
from app.models.work_item import WorkItem
from datetime import datetime
import json

router = APIRouter()

@router.post("/signal")
def ingest_signal(signal: dict):
    db = SessionLocal()

    component_id = signal.get("component_id")

    if not component_id:
        return {"error": "component_id is required"}

    signal["received_at"] = datetime.utcnow().isoformat()

    redis_key = f"debounce:{component_id}"

    if redis_client.exists(redis_key):
        # Existing group
        redis_client.rpush(redis_key, json.dumps(signal))
        status = "merged_with_existing"

        # Get existing work item id
        work_item_id = redis_client.get(f"workitem:{component_id}")

    else:
        # New group → create Work Item
        redis_client.rpush(redis_key, json.dumps(signal))
        redis_client.expire(redis_key, 60)

        new_work = WorkItem(component_id=component_id)
        db.add(new_work)
        db.commit()
        db.refresh(new_work)

        # Store mapping in Redis
        redis_client.set(f"workitem:{component_id}", new_work.id)

        work_item_id = new_work.id
        status = "new_work_item_created"

    # Always store raw signal
    signal["work_item_id"] = work_item_id
    signals_collection.insert_one(signal)

    db.close()

    return {
        "message": "Signal processed",
        "status": status,
        "work_item_id": work_item_id
    }
