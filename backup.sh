#!/usr/bin/env bash
set -e
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo "Dumping Postgres DB to backups/db_${TIMESTAMP}.sql"
mkdir -p backups
docker exec -t $(docker compose ps -q postgres) pg_dump -U app appdb > backups/db_${TIMESTAMP}.sql
echo "Backup complete: backups/db_${TIMESTAMP}.sql"
