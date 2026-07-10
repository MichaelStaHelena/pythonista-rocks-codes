# pip install httpx httpx-retries
import asyncio
import httpx
from httpx_retries import Retry, RetryTransport, AsyncRetryTransport

# ── Sync client ──────────────────────────────────────────────────────────────
retry = Retry(total=3, backoff_factor=0.5)
# Retry schedule for backoff_factor=0.5:
#   attempt 1 → immediate, attempt 2 → 0.5 s, attempt 3 → 1.0 s, attempt 4 → 2.0 s

transport = RetryTransport(retry=retry)

with httpx.Client(transport=transport, timeout=httpx.Timeout(connect=2.0, read=10.0, write=5.0, pool=1.0)) as client:
    try:
        response = client.get("https://httpbin.org/status/503")
        print(response.status_code)  # => 503 only if all retries exhausted
        # RetryTransport retries on 5xx by default; raises after total attempts.
    except httpx.HTTPStatusError as exc:
        print(f"Failed after retries: {exc.response.status_code}")
    # Note: timeout= applies PER ATTEMPT, not across the whole retry sequence.

# ── Async client ─────────────────────────────────────────────────────────────
async def fetch():
    async_transport = AsyncRetryTransport(retry=Retry(total=3, backoff_factor=0.5))
    async with httpx.AsyncClient(transport=async_transport, timeout=10.0) as client:
        try:
            r = await client.get("https://httpbin.org/status/503")
            print(r.status_code)
        except httpx.HTTPStatusError as exc:
            print(f"Async failed after retries: {exc.response.status_code}")

asyncio.run(fetch())

# ── THE TRAP ─────────────────────────────────────────────────────────────────
# This looks like it retries on everything, but it does NOT:
transport_builtin = httpx.HTTPTransport(retries=3)
# retries=3 ONLY covers: httpx.ConnectError and httpx.ConnectTimeout.
# A 503 response comes back immediately — zero retries.
# A ReadTimeout raises immediately — zero retries.
# If you're coming from requests' HTTPAdapter(max_retries=3), this will bite you.
print("HTTPTransport(retries=3) built-in scope: ConnectError + ConnectTimeout only")
# => HTTPTransport(retries=3) built-in scope: ConnectError + ConnectTimeout only
