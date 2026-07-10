# pip install python-dateutil
from dateutil import parser as du_parser
from dateutil.relativedelta import relativedelta
import datetime

# Fuzzy / human-readable string parsing (no exact format needed)
dt1 = du_parser.parse("July 30, 2025 3pm")
print("parse 1 :", dt1)
# => parse 1 : 2025-07-30 15:00:00

dt2 = du_parser.parse("30 Jul 2025 15:00")
print("parse 2 :", dt2)
# => parse 2 : 2025-07-30 15:00:00

# relativedelta: "add 1 month" — timedelta(days=31) would overshoot February
start = datetime.datetime(2025, 1, 31)
print("Jan 31 + 1 month :", (start + relativedelta(months=1)).date())
# => Jan 31 + 1 month : 2025-02-28

# Add 1 year
print("anniversary +1yr :", (start + relativedelta(years=1)).date())
# => anniversary +1yr : 2026-01-31
