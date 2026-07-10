import httpx

# httpx enforces max_connections with a semaphore — requests beyond the cap
# block (or raise PoolTimeout) rather than silently opening extra connections.
limits = httpx.Limits(
    max_connections=100,           # hard cap enforced by asyncio.Semaphore
    max_keepalive_connections=20,  # idle keep-alive slots retained
    keepalive_expiry=5.0,          # seconds before an idle conn is closed
)
print("max_connections         :", limits.max_connections)           # => 100
print("max_keepalive_connections:", limits.max_keepalive_connections) # => 20
print("keepalive_expiry        :", limits.keepalive_expiry)           # => 5.0
