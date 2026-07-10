import datetime

naive = datetime.datetime(2025, 7, 4, 12, 0, 0)
aware = datetime.datetime(2025, 7, 4, 12, 0, 0, tzinfo=datetime.UTC)

print("naive tzinfo :", naive.tzinfo)
# => naive tzinfo : None
print("aware tzinfo :", aware.tzinfo)
# => aware tzinfo : UTC

try:
    diff = aware - naive          # mixing naive and aware → TypeError
except TypeError as e:
    print("TypeError    :", e)
# => TypeError    : can't subtract offset-naive and offset-aware datetimes
