import datetime

today = datetime.date.today()
print("date      :", today)
# => date      : 2026-07-10

t = datetime.time(14, 30, 0)
print("time      :", t)
# => time      : 14:30:00

dt = datetime.datetime(2025, 3, 9, 14, 30, 0)
print("datetime  :", dt)
# => datetime  : 2025-03-09 14:30:00

delta = datetime.timedelta(days=7, hours=3)
print("timedelta :", delta)
# => timedelta : 7 days, 3:00:00
