import httpx

# Fine-grained timeout: each network phase gets its own budget.
# connect: time to open the TCP socket (DNS lookup not included)
# read:    time to wait for each chunk of response data
# write:   time to fully send the request body
# pool:    time to wait for a free connection from the pool
timeout = httpx.Timeout(connect=2.0, read=10.0, write=5.0, pool=1.0)

print(repr(timeout))
# => Timeout(connect=2.0, read=10.0, write=5.0, pool=1.0)
print(timeout.connect)  # => 2.0
print(timeout.read)     # => 10.0
print(timeout.write)    # => 5.0
print(timeout.pool)     # => 1.0

# Always use Client as a context manager to avoid connection leaks.
with httpx.Client(timeout=timeout) as client:
    try:
        response = client.get("https://httpbin.org/delay/15")  # will time out
    except httpx.ReadTimeout:
        # Catch the specific subtype when you want to handle it differently
        # (e.g. retry only on ReadTimeout, not on ConnectTimeout).
        print("Server stopped sending data within the read window.")
        # => Server stopped sending data within the read window.
    except httpx.ConnectTimeout:
        print("Could not open a connection in time.")
    except httpx.TimeoutException as exc:
        # TimeoutException is the base class for all four phases.
        # Catch this when you want to handle any timeout the same way.
        print(f"Request timed out ({type(exc).__name__})")

# Shorthand: one float applies the same budget to all four phases.
# Use this when you don't need per-phase control.
with httpx.Client(timeout=5.0) as client:
    pass  # fine for simple scripts; prefer explicit Timeout in production

# Never do this in production code:
# httpx.Client(timeout=None)  # disables all timeouts — hangs forever on a slow server
