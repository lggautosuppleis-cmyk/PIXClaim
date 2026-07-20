# Connector: NHTSA VPIC - VIN decode
from src.connectors.fetcher import fetch_json
from src.connectors.schemas import VehicleRecord
from src.services.database import upsert_vehicle_record
from src.services.redis_pub import publish_event

VPIC_BASE = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValues/"

async def ingest_vin(vin: str):
    url = f"{VPIC_BASE}{vin}?format=json"
    data, headers = await fetch_json(url)
    results = data.get("Results", [{}])[0]
    rec = VehicleRecord(
        vin=vin,
        make=results.get("Make"),
        model=results.get("Model"),
        model_year=int(results.get("ModelYear")) if results.get("ModelYear") else None,
        trim=results.get("Trim"),
        body_class=results.get("BodyClass"),
        raw=results
    )
    await upsert_vehicle_record(rec)
    await publish_event("data.ingested.nhtsa_vpic", {"source":"nhtsa_vpic","vin":vin})
    return rec
