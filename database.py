# Minimal async DB persistence (SQLAlchemy async) - upsert examples
import os
import json
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, future=True, echo=False)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def upsert_vehicle_record(rec):
    async with AsyncSessionLocal() as session:
        await session.execute(text("""
        INSERT INTO vehicles(vin, make, model, model_year, trim, body_class, raw)
        VALUES(:vin,:make,:model,:model_year,:trim,:body_class,:raw)
        ON CONFLICT (vin) DO UPDATE SET make=EXCLUDED.make, model=EXCLUDED.model, model_year=EXCLUDED.model_year, raw=EXCLUDED.raw;
        """), {"vin":rec.vin,"make":rec.make,"model":rec.model,"model_year":rec.model_year,"trim":rec.trim,"body_class":rec.body_class,"raw":json.dumps(rec.raw)})
        await session.commit()

async def upsert_recall_record(rec):
    async with AsyncSessionLocal() as session:
        await session.execute(text("""
        INSERT INTO recalls(recall_id, vin, make, model, year, component, summary, remedy, raw)
        VALUES(:recall_id,:vin,:make,:model,:year,:component,:summary,:remedy,:raw)
        ON CONFLICT (recall_id) DO UPDATE SET summary=EXCLUDED.summary, remedy=EXCLUDED.remedy, raw=EXCLUDED.raw;
        """), {"recall_id":rec.recall_id,"vin":rec.vin,"make":rec.make,"model":rec.model,"year":rec.year,"component":rec.component,"summary":rec.summary,"remedy":rec.remedy,"raw":json.dumps(rec.raw)})
        await session.commit()
