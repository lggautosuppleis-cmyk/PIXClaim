# PixClaim — MVP Agents Skeleton

Estructura mínima para ejecutar los agentes IA orquestados por Redis pub/sub.

Requisitos:
- Docker & Docker Compose
- Python 3.11 (para desarrollo local)
- Tener disponible la variable STRIPE_API_KEY en .env

Pasos rápidos:
1. Copia `.env.example` a `.env` y ajusta valores.
2. Construir y levantar:
   docker compose up -d --build
3. API: http://localhost:8000/docs (Swagger)

Comandos útiles:
- Levantar logs:
  docker compose logs -f api
- Ejecutar tests:
  pytest -q

Siguientes pasos:
- Añadir worker/vision, Weaviate y MinIO a la composición.
- Completar integración Stripe y endpoints reales de Redis.
