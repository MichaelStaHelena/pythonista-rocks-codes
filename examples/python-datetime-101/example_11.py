# pip install pendulum
import pendulum

# Always timezone-aware — naive datetimes are a non-issue by design
p = pendulum.datetime(2025, 7, 4, 12, 0, 0, tz="America/New_York")
print("datetime :", p.isoformat())
# => datetime : 2025-07-04T12:00:00-04:00
print("tz name  :", p.timezone_name)
# => tz name  : America/New_York

# Month arithmetic respects DST and calendar boundaries
print("+1 month :", p.add(months=1).isoformat())
# => +1 month : 2025-08-04T12:00:00-04:00

# Human-readable diff
ref_p  = pendulum.datetime(2025, 7, 4, 12, 0, 0, tz="UTC")
past_p = pendulum.datetime(2025, 6, 4, 12, 0, 0, tz="UTC")
print("diff     :", past_p.diff_for_humans(ref_p))
# => diff     : 1 month ago

# Convert zone
print("→ Berlin :", p.in_timezone("Europe/Berlin").isoformat())
# => → Berlin : 2025-07-04T18:00:00+02:00
