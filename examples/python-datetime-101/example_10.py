# pip install arrow
import arrow

# UTC now and ISO formatting
now = arrow.utcnow()
print("type     :", type(now).__name__)
# => type     : Arrow

# Parse a string — always pass the format to avoid DD/MM vs MM/DD ambiguity
a = arrow.get("2025-07-04", "YYYY-MM-DD")
print("parsed   :", a.isoformat())
# => parsed   : 2025-07-04T00:00:00+00:00

# Shift (returns a new Arrow object)
shifted = a.shift(hours=+9)
print("shift +9h:", shifted.isoformat())
# => shift +9h: 2025-07-04T09:00:00+00:00

# Convert to another timezone
print("→ Tokyo  :", a.to("Asia/Tokyo").format("YYYY-MM-DD HH:mm ZZZ"))
# => → Tokyo  : 2025-07-04 09:00 JST

# Humanize (relative description between two fixed Arrow objects)
ref  = arrow.Arrow(2025, 7, 4, 12, 0, 0, tzinfo="UTC")
past = arrow.Arrow(2025, 7, 4,  9, 0, 0, tzinfo="UTC")
print("humanize :", past.humanize(ref))
# => humanize : 3 hours ago
