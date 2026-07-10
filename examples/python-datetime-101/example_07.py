import datetime
from zoneinfo import ZoneInfo

# Windows users: pip install tzdata
# Linux / macOS: works out of the box

ny     = ZoneInfo("America/New_York")
london = ZoneInfo("Europe/London")

# A UTC moment …
meeting_utc = datetime.datetime(2025, 7, 4, 17, 0, tzinfo=datetime.UTC)

# … displayed in different local times
meeting_ny  = meeting_utc.astimezone(ny)
meeting_lon = meeting_utc.astimezone(london)

print("UTC    :", meeting_utc.strftime("%H:%M %Z"))
# => UTC    : 17:00 UTC
print("NY     :", meeting_ny.strftime("%H:%M %Z"))
# => NY     : 13:00 EDT
print("London :", meeting_lon.strftime("%H:%M %Z"))
# => London : 18:00 BST

# Attach a zone at construction time
dt_ny = datetime.datetime(2025, 7, 4, 13, 0, tzinfo=ny)
print("NY ctor:", dt_ny.strftime("%H:%M %Z"))
# => NY ctor: 13:00 EDT
print("as UTC :", dt_ny.astimezone(datetime.UTC).strftime("%H:%M %Z"))
# => as UTC : 17:00 UTC
