# Simple fetcher reutilizable con backoff, ETag support
import httpx
import asyncio

async def fetch_json(url: str, params: dict = None, headers: dict = None, timeout: int = 30, retries: int = 3):
    headers = headers or {}
    params = params or {}
    backoff = 1.0
    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in range(retries):
            try:
                r = await client.get(url, params=params, headers=headers)
                r.raise_for_status()
                return r.json(), r.headers
            except httpx.HTTPStatusError as e:
                if 400 <= e.response.status_code < 500 and e.response.status_code != 429:
                    raise
                await asyncio.sleep(backoff)
                backoff *= 2
            except Exception:
                await asyncio.sleep(backoff)
                backoff *= 2
    raise RuntimeError(f"Failed fetching {url} after {retries} attempts")
