import threading, requests
from concurrent.futures import ThreadPoolExecutor

# Canned response — no network needed
class MockAdapter(requests.adapters.HTTPAdapter):
    def send(self, request, **kwargs):
        from requests.models import Response
        r = Response()
        r.status_code = 200
        r._content = b'{"mocked": true}'
        return r

_local = threading.local()

def fetch(url: str) -> int:
    # Each thread owns its own Session; sharing one Session is NOT thread-safe
    # because Session.headers, .cookies and .auth are mutable shared state.
    if not hasattr(_local, "session"):
        _local.session = requests.Session()
        _local.session.mount("https://", MockAdapter())
    return _local.session.get(url).status_code   # => 200

urls = [f"https://api.example.com/item/{i}" for i in range(10)]
with ThreadPoolExecutor(max_workers=4) as pool:
    statuses = list(pool.map(fetch, urls))

print(f"Responses : {len(statuses)}")                           # => 10
print(f"All 200   : {all(s == 200 for s in statuses)}")         # => True
