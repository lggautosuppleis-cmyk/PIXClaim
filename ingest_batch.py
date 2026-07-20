#!/usr/bin/env python3
"""Batch ingest script example"""
import argparse
import csv
import asyncio
from src.connectors.nhtsa_vpic import ingest_vin

async def run_batch(file):
    vins = []
    with open(file) as f:
        r = csv.reader(f)
        for row in r:
            if row:
                vins.append(row[0].strip())
    for vin in vins:
        try:
            await ingest_vin(vin)
            print("ingested", vin)
        except Exception as e:
            print("error", vin, e)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--file', required=True)
    args = p.parse_args()
    asyncio.run(run_batch(args.file))
