import requests, inspect

# requests.api.get() is a thin wrapper that calls request(), which
# internally creates a *new* Session on every invocation — no pooling.
src = inspect.getsource(requests.api.get)
print(src[:300])
# The key line inside: `with sessions.Session() as session:`
# Each top-level call = a fresh TCP connection. Use a long-lived Session.
