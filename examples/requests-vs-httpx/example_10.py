import inspect, requests
from requests.auth import AuthBase, HTTPBasicAuth

# AuthBase defines a single __call__ that mutates a PreparedRequest in-place.
# Multi-step auth (digest, OAuth) requires inspecting the Response externally
# and reissuing a request — there is no built-in generator protocol.
print("AuthBase MRO:", [c.__name__ for c in AuthBase.__mro__])
# => ['AuthBase', 'object']
print("HTTPBasicAuth.__call__ sig:", inspect.signature(HTTPBasicAuth.__call__))
# => (self, r: 'PreparedRequest') -> 'PreparedRequest'
