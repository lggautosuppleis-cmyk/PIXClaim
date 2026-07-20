#!/usr/bin/env bash
set -e
echo "Starting PixClaim stack (docker-compose)..."
docker compose up -d --build
echo "All services requested. Use 'docker compose logs -f' to follow."
