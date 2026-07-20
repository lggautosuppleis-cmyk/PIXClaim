# Connector: NHTSA Recalls
from src.connectors.fetcher import fetch_json
from src.connectors.schemas import RecallRecord
from src.services.database import upsert_recall_record
from src.services.redis_pub import publish_event

RECALL_BASE = "https://api.nhtsa.gov/recalls/recallsByVin/"

async def ingest_recalls_by_vin(vin: str):
    url = f"{RECALL_BASE}{vin}"
    data, headers = await fetch_json(url)
    results = data.get("results", [])
    saved = []
    for r in results:
        rec = RecallRecord(
            recall_id=r.get("NHTSACampaignNumber") or r.get("ReportReceivedDate") or r.get("RecallNumber",""),
            vin=vin,
            make=r.get("Make"),
            model=r.get("Model"),
            year=r.get("ModelYear"),
            component=r.get("Component"),
            summary=r.get("Summary"),
            remedy=r.get("Remedy"),
            raw=r
        )
        await upsert_recall_record(rec)
        saved.append(rec)
    await publish_event("data.ingested.nhtsa_recalls", {"source":"nhtsa_recalls","vin":vin,"count":len(saved)})
    return saved
