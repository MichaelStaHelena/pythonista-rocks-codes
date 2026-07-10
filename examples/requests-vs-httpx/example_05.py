import requests, httpx

# requests: only connect + read; no write timeout, no pool-wait timeout
timeout_requests = (2.5, 10.0)   # (connect, read)
print("requests timeout tuple:", timeout_requests)   # => (2.5, 10.0)

# httpx: four independent phases
t = httpx.Timeout(connect=2.5, read=10.0, write=5.0, pool=1.0)
print("httpx Timeout.connect:", t.connect)  # => 2.5
print("httpx Timeout.read   :", t.read)     # => 10.0
print("httpx Timeout.write  :", t.write)    # => 5.0
# pool = max wait for a free slot from the connection semaphore;
# exceeding it raises httpx.PoolTimeout (no equivalent in requests).
print("httpx Timeout.pool   :", t.pool)     # => 1.0
