import httpx

class TokenRefreshAuth(httpx.Auth):
    """
    Round-trip 1: attach the current Bearer token, send the request.
    If the server returns 401, refresh the token and yield a second request.
    One yield = one network round-trip — the protocol is explicit and testable.
    """
    def __init__(self, token: str) -> None:
        self.token = token

    def auth_flow(self, request: httpx.Request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        response = yield request                    # ← round-trip 1

        if response.status_code == 401:
            self.token = "refreshed-token"          # call token endpoint here
            request.headers["Authorization"] = f"Bearer {self.token}"
            yield request                           # ← round-trip 2

# Drive the generator manually to verify the protocol
auth = TokenRefreshAuth("initial-token")
flow = auth.auth_flow(httpx.Request("GET", "https://api.example.com/data"))

first = next(flow)
print("Round-trip 1 header:", first.headers["authorization"])
# => Bearer initial-token

second = flow.send(httpx.Response(401))   # simulate 401
print("Round-trip 2 header:", second.headers["authorization"])
# => Bearer refreshed-token
