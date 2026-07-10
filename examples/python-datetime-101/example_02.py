import datetime

# Naive — no timezone info (tzinfo is None)
now_naive = datetime.datetime.now()
print("naive tzinfo :", now_naive.tzinfo)
# => naive tzinfo : None

# Aware UTC — the preferred default for all new code (Python 3.12+)
now_utc = datetime.datetime.now(datetime.UTC)
print("UTC   tzinfo :", now_utc.tzinfo)
# => UTC   tzinfo : UTC

# Constructor with explicit UTC
dt = datetime.datetime(2025, 7, 4, 9, 0, 0, tzinfo=datetime.UTC)
print("constructed  :", dt)
# => constructed  : 2025-07-04 09:00:00+00:00
