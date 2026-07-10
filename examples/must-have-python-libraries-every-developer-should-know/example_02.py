import requests
from unittest.mock import patch, MagicMock

def fetch_joke(timeout: int = 10) -> dict:
    resp = requests.get(
        "https://official-joke-api.appspot.com/random_joke",
        timeout=timeout,          # ⚠️ omitting this can freeze your script forever
    )
    resp.raise_for_status()       # ⚠️ without this, a 404 or 500 will NOT raise
    return resp.json()

# --- happy path (200) ---
mock_ok = MagicMock()
mock_ok.status_code = 200
mock_ok.raise_for_status = MagicMock()   # no-op: 200 is fine
mock_ok.json.return_value = {
    "id": 1, "type": "general",
    "setup": "Why did the dev quit?",
    "punchline": "No exceptions.",
}
with patch("requests.get", return_value=mock_ok):
    joke = fetch_joke()

print("joke setup:", joke["setup"])      # => joke setup: Why did the dev quit?
print("joke punchline:", joke["punchline"])  # => joke punchline: No exceptions.

# --- 404 path: raise_for_status() turns the silent failure into a real exception ---
mock_404 = MagicMock()
mock_404.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
with patch("requests.get", return_value=mock_404):
    try:
        r = requests.get("https://example.com/bad", timeout=10)
        r.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        print("caught HTTPError:", exc)   # => caught HTTPError: 404 Client Error
