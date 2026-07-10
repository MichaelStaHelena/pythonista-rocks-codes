import httpx

# --- Sync: almost identical to requests ---
r = httpx.get("https://httpbin.org/get", timeout=10)   # httpx default is 5 s — raise it for slow APIs
print("status:", r.status_code)                         # => status: 200
print("http version:", r.http_version)                  # => http version: HTTP/1.1

# --- Async: the real reason to choose httpx ---
import asyncio

async def fetch_many(urls: list[str]) -> list[int]:
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [resp.status_code for resp in responses]

codes = asyncio.run(fetch_many([
    "https://httpbin.org/get",
    "https://httpbin.org/ip",
]))
print("status codes:", codes)   # => status codes: [200, 200]
