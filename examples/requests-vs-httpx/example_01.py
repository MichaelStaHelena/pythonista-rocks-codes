import requests
from requests.adapters import HTTPAdapter
from requests import Session

# Every request passes through prepare_request() first.
# The result is a frozen, fully-assembled HTTP message.
req = requests.Request("GET", "https://httpbin.org/get", headers={"X-Custom": "demo"})
prepared = req.prepare()

print("PreparedRequest type  :", type(prepared).__name__)   # => PreparedRequest
print("PreparedRequest.method:", prepared.method)           # => GET
print("PreparedRequest.url   :", prepared.url)              # => https://httpbin.org/get

# Session.get_adapter() sorts all mounted prefixes by length (descending)
# and returns the first match — longest prefix wins.
s = Session()

a_specific = HTTPAdapter()   # handles /v2/ only
a_general  = HTTPAdapter()   # handles everything else under api.example.com

s.mount("https://api.example.com/v2/", a_specific)
s.mount("https://api.example.com/",    a_general)

picked = s.get_adapter("https://api.example.com/v2/users")
print("Longest-prefix adapter picked:", picked is a_specific)  # => True
