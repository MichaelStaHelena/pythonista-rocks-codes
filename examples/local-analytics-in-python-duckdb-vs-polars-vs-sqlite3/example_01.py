import csv
import os
import time
import numpy as np

rng = np.random.default_rng(42)
N = 1_000_000

REGIONS = [
    "North", "South", "East", "West", "Central",
    "Northwest", "Southeast", "Midwest", "Southwest", "Northeast",
]
CATEGORIES = [f"Cat_{i:02d}" for i in range(50)]

order_ids    = np.arange(1, N + 1)
regions      = rng.choice(REGIONS, size=N)
categories   = rng.choice(CATEGORIES, size=N)
sale_amounts = np.round(rng.uniform(10.0, 2000.0, size=N), 2)

base_date  = np.datetime64("2023-01-01")
offsets    = rng.integers(0, 730, size=N)
sale_dates = [str(base_date + np.timedelta64(int(d), "D")) for d in offsets]

CSV_PATH = "/tmp/sales_1m.csv"

t0 = time.perf_counter()
with open(CSV_PATH, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["order_id", "region", "product_category", "sale_amount", "sale_date"])
    for i in range(N):
        writer.writerow(
            [order_ids[i], regions[i], categories[i], sale_amounts[i], sale_dates[i]]
        )
elapsed = time.perf_counter() - t0

size_mb = os.path.getsize(CSV_PATH) / (1024 * 1024)
print(f"Rows written : {N:,}")         # => Rows written : 1,000,000
print(f"CSV size     : {size_mb:.1f} MB")  # => ...
print(f"Write time   : {elapsed:.2f}s")    # => ...
