import datetime

# ❌  Old — deprecated since Python 3.12, returns a NAIVE datetime
# datetime.datetime.utcnow()   # DeprecationWarning

# ✅  New — always use this instead
now = datetime.datetime.now(datetime.UTC)
print("tzinfo :", now.tzinfo)
# => tzinfo : UTC
print("aware  :", now.utcoffset())
# => aware  : 0:00:00
