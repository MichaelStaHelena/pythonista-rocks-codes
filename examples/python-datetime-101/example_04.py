import datetime

dt = datetime.datetime(2025, 7, 4, 9, 0, 0, tzinfo=datetime.UTC)

iso = dt.isoformat()
print("isoformat        :", iso)
# => isoformat        : 2025-07-04T09:00:00+00:00

back = datetime.datetime.fromisoformat(iso)
print("fromisoformat    :", back)
# => fromisoformat    : 2025-07-04 09:00:00+00:00

# Python 3.11+ understands the trailing Z
back_z = datetime.datetime.fromisoformat("2025-07-04T09:00:00Z")
print("fromisoformat Z  :", back_z)
# => fromisoformat Z  : 2025-07-04 09:00:00+00:00
