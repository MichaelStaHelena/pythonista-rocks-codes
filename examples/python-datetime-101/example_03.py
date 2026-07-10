import datetime

dt = datetime.datetime(2025, 7, 4, 9, 5, 0)

# ⚠️  %Y (four-digit) vs %y (two-digit)
print("4-digit year :", dt.strftime("%Y-%m-%d"))
# => 4-digit year : 2025-07-04
print("2-digit year :", dt.strftime("%y-%m-%d"))
# => 2-digit year : 25-07-04

# ⚠️  %m (month 01-12) vs %M (minutes 00-59) — very common bug
print("month vs min :", dt.strftime("month=%m  minute=%M"))
# => month vs min : month=07  minute=05

# 12-hour clock with AM/PM
print("12-hour      :", dt.strftime("%I:%M %p"))
# => 12-hour      : 09:05 AM

# Human-readable full date
print("human        :", dt.strftime("%A, %B %d %Y"))
# => human        : Friday, July 04 2025

# strptime: parse a string into a datetime
parsed = datetime.datetime.strptime("30, July 2025", "%d, %B %Y")
print("strptime     :", parsed)
# => strptime     : 2025-07-30 00:00:00
