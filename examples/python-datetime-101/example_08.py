import datetime
from zoneinfo import ZoneInfo

ny = ZoneInfo("America/New_York")

# Basic arithmetic
base = datetime.datetime(2025, 7, 4, 12, 0, 0, tzinfo=datetime.UTC)
print("in 2 weeks  :", (base + datetime.timedelta(weeks=2)).date())
# => in 2 weeks  : 2025-07-18
print("3 hours ago :", (base - datetime.timedelta(hours=3)).strftime("%H:%M %Z"))
# => 3 hours ago : 09:00 UTC

# ── DST worked example: "spring forward" night in New York ───────────────────
# 2025-03-09: clocks jump from 02:00 EST → 03:00 EDT (one hour is skipped)
start = datetime.datetime(2025, 3, 9, 0, 0, tzinfo=ny)
print("\nStart       :", start.strftime("%Y-%m-%d %H:%M %Z (UTC%z)"))
# => Start       : 2025-03-09 00:00 EST (UTC-0500)

# timedelta(days=1) always means exactly 86 400 real seconds — correct
plus_one = start + datetime.timedelta(days=1)
print("+1 day      :", plus_one.strftime("%Y-%m-%d %H:%M %Z (UTC%z)"))
# => +1 day      : 2025-03-10 00:00 EDT (UTC-0400)

# ⚠️  The dangerous anti-pattern: strip tz → add → re-attach with replace()
naive_stripped = start.replace(tzinfo=None)                  # loses zone
naive_plus1    = naive_stripped + datetime.timedelta(days=1)
wrong_result   = naive_plus1.replace(tzinfo=ny)              # blindly stamps zone
print("\n❌ wrong (replace):", wrong_result.strftime("%Y-%m-%d %H:%M %Z (UTC%z)"))
# => ❌ wrong (replace): 2025-03-10 00:00 EDT (UTC-0400)

# ✅  Safe pattern: work in UTC throughout, convert to local only for display
safe_result = (
    start.astimezone(datetime.UTC)          # convert to UTC
    + datetime.timedelta(days=1)            # add 24 real hours in UTC
).astimezone(ny)                            # back to local only at the end
print("✅ safe  (UTC)    :", safe_result.strftime("%Y-%m-%d %H:%M %Z (UTC%z)"))
# => ✅ safe  (UTC)    : 2025-03-10 01:00 EDT (UTC-0400)
