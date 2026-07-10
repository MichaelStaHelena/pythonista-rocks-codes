import requests

# ✗ WRONG — hangs forever if the server stalls
# r = requests.get("https://api.example.com/data")

# ✓ RIGHT — always supply an explicit timeout (seconds)
try:
    r = requests.get("https://httpbin.org/get", timeout=5)
    print("status:", r.status_code)           # => status: 200
    print("Content-Type:", r.headers["Content-Type"])  # => Content-Type: application/json
except requests.exceptions.Timeout:
    print("request timed out — retry or raise")
