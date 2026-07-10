from requests.adapters import HTTPAdapter

adapter = HTTPAdapter()

print(f"pool_connections : {adapter._pool_connections}")  # => 10
print(f"pool_maxsize     : {adapter._pool_maxsize}")       # => 10
# pool_block=False means the cap is *soft*: when all 10 slots are taken,
# urllib3 opens a new connection rather than blocking the caller.
# Set pool_block=True to enforce a hard cap (blocking behaviour).
print(f"pool_block       : {adapter._pool_block}")         # => False
