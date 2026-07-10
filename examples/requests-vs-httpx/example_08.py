import requests
from requests.adapters import HTTPAdapter
from requests import PreparedRequest

class LoggingAdapter(HTTPAdapter):
    # send() signature is tightly coupled to urllib3 internals:
    # (request, stream, timeout, verify, cert, proxies)
    def send(self, request: PreparedRequest, *args, **kwargs):
        print(f"→ {request.method} {request.url}")
        return super().send(request, *args, **kwargs)

s = requests.Session()
s.mount("https://", LoggingAdapter())
# The adapter is wired; send() carries urllib3-specific keyword arguments
# that leak the underlying transport's abstractions.
print("LoggingAdapter mounted; send() takes PreparedRequest + urllib3 kwargs")
# => LoggingAdapter mounted; send() takes PreparedRequest + urllib3 kwargs
