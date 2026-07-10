import asyncio, httpx

async def simple_asgi_app(scope, receive, send):
    """Minimal raw ASGI callable — stands in for any FastAPI/Starlette app."""
    assert scope["type"] == "http"
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"application/json")],
    })
    await send({"type": "http.response.body", "body": b'{"asgi": true}'})

async def test_app():
    # httpx 0.28 removed the `app=` shortcut from Client/AsyncClient.
    # The canonical form is always: transport=httpx.ASGITransport(app=...)
    transport = httpx.ASGITransport(app=simple_asgi_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.get("/health")
        return resp.status_code, resp.json()

status, body = asyncio.run(test_app())
print("status:", status)   # => 200
print("body  :", body)     # => {'asgi': True}
