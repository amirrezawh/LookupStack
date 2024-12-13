from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import IPLookup
from app.utils import fetch_region_from_api
from sqlalchemy import select
from prometheus_client import Counter

router = APIRouter()

ip_lookup_requests = Counter("ip_lookup_requests", "Count of IP lookup requests", ["source"])
ip_lookup_failures = Counter("ip_lookup_failures", "Count of failed IP lookups", ["reason"])

@router.get("/get-region/{ip_address}")
def get_region(ip_address: str, db: Session = Depends(get_db)):
    ip_lookup_requests.labels(source="api_call").inc()

    query = select(IPLookup).where(IPLookup.ip_address == ip_address)
    result = db.execute(query).scalar_one_or_none()

    if result:
        return {"ip_address": ip_address, "region": result.region}

    try:
        region = fetch_region_from_api(ip_address)
    except HTTPException as e:
        ip_lookup_failures.labels(reason="api_failure").inc()
        raise e

    new_entry = IPLookup(ip_address=ip_address, region=region)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return {"ip_address": ip_address, "region": region}

