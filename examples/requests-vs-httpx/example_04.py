import requests, httpx

payload = {"library": "requests", "version": 2}

# requests uses Python's json.dumps default: spaces after separators
req_prep = requests.Request("POST", "https://httpbin.org/post", json=payload).prepare()
print("requests body:", req_prep.body.decode())
# => {"library": "requests", "version": 2}

# httpx 0.28+ switched to compact representation (no spaces after : or ,)
# This is a silent breaking change for tests asserting on exact body bytes.
httpx_req = httpx.Request("POST", "https://httpbin.org/post", json=payload)
print("httpx    body:", httpx_req.content.decode())
# => {"library":"requests","version":2}
