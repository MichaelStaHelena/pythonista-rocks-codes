import httpx

class FixedResponseTransport(httpx.BaseTransport):
    """Return a canned response without touching the network.
    The entire contract is a single method: handle_request → Response.
    Compare with requests' HTTPAdapter.send(), which is coupled to
    urllib3 kwargs (stream, verify, cert, proxies, timeout).
    """
    def handle_request(self, request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"mocked": True, "path": request.url.path},
        )

with httpx.Client(transport=FixedResponseTransport()) as client:
    resp = client.get("https://example.com/ping")

print("status:", resp.status_code)   # => 200
print("body  :", resp.json())        # => {'mocked': True, 'path': '/ping'}
