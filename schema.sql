-- Minimal schema for vehicles and recalls
CREATE TABLE IF NOT EXISTS vehicles (
  vin TEXT PRIMARY KEY,
  make TEXT,
  model TEXT,
  model_year INTEGER,
  trim TEXT,
  body_class TEXT,
  raw JSONB,
  ingested_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS recalls (
  recall_id TEXT PRIMARY KEY,
  vin TEXT,
  make TEXT,
  model TEXT,
  year INTEGER,
  component TEXT,
  summary TEXT,
  remedy TEXT,
  raw JSONB,
  ingested_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ingestion_log (
  id SERIAL PRIMARY KEY,
  source TEXT,
  key TEXT,
  raw_hash TEXT,
  status TEXT,
  created_at TIMESTAMP DEFAULT now()
);
