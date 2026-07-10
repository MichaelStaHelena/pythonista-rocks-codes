import asyncio, time
import httpx

# ── Fake transport: 10 ms latency, no network ─────────────────────────────────
class TimingTransport(httpx.AsyncBaseTransport):
    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        await asyncio.sleep(0.01)
        return httpx.Response(200, json={"url": str(request.url)})

timings: dict[str, float] = {}

# Async event hooks *must* be coroutines when used with AsyncClient
async def on_request(request: httpx.Request) -> None:
    request.extensions["start_ts"] = time.perf_counter()   # type: ignore[index]

async def on_response(response: httpx.Response) -> None:
    start = response.request.extensions.get("start_ts", 0.0)
    timings[str(response.request.url)] = time.perf_counter() - start

async def async_fan_out() -> list[httpx.Response]:
    limits  = httpx.Limits(max_connections=5, max_keepalive_connections=5)
    timeout = httpx.Timeout(connect=2.0, read=5.0, write=2.0, pool=2.0)
    async with httpx.AsyncClient(
        transport=TimingTransport(),
        limits=limits,
        timeout=timeout,
        event_hooks={"request": [on_request], "response": [on_response]},
    ) as client:
        urls = [f"https://api.example.com/item/{i}" for i in range(10)]
        return await asyncio.gather(*[client.get(u) for u in urls])

results = asyncio.run(async_fan_out())
print(f"Fan-out responses     : {len(results)}")         # => 10
print(f"All 200               : {all(r.status_code == 200 for r in results)}")  # => True
print(f"Timing entries        : {len(timings)}")         # => 10
print(f"All per-request t > 0 : {all(v > 0 for v in timings.values())}")        # => True

# ── PoolTimeout when the semaphore cap is saturated ───────────────────────────
class SlowTransport(httpx.AsyncBaseTransport):
    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        await asyncio.sleep(10)
        return httpx.Response(200)

async def pool_timeout_demo() -> str:
    limits  = httpx.Limits(max_connections=1, max_keepalive_connections=1)
    # pool=0.05 s: second request waits at most 50 ms for a free connection slot
    timeout = httpx.Timeout(connect=5.0, read=5.0, write=5.0, pool=0.05)
    async with httpx.AsyncClient(
        transport=SlowTransport(), limits=limits, timeout=timeout,
    ) as client:
        try:
            await asyncio.gather(
                client.get("https://example.com/slow"),
                client.get("https://example.com/blocked"),
            )
        except httpx.PoolTimeout as exc:
            return f"PoolTimeout raised: {type(exc).__name__}"
    return "no timeout"

print(asyncio.run(pool_timeout_demo()))   # => PoolTimeout raised: PoolTimeout
