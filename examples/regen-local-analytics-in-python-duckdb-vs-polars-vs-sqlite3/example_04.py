import polars as pl
import csv, random, os

random.seed(42)
N = 20_000
CSV_PATH = "trips.csv"

with open(CSV_PATH, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["pickup_hour", "passenger_count", "trip_distance", "total_amount"])
    for _ in range(N):
        w.writerow([
            random.randint(0, 23),
            random.randint(0, 4),
            round(random.uniform(0.5, 20.0), 2),
            round(random.uniform(3.0, 80.0), 2),
        ])

lf = (
    pl.scan_csv(CSV_PATH)
      .filter(pl.col("passenger_count") > 0)
      .group_by("pickup_hour")
      .agg(
          pl.len().alias("trip_count"),
          pl.col("trip_distance").mean().round(4).alias("avg_distance"),
          pl.col("total_amount").sum().round(2).alias("total_revenue"),
      )
      .sort("pickup_hour")
)

print("=== Unoptimized logical plan ===")  # => =================================== Unoptimized logical plan ===
print(lf.explain(optimized=False))         # => ...
print()                                    # => ...
print("=== Optimized logical plan ===")   # => =================================== Optimized logical plan ===
print(lf.explain(optimized=True))         # => ...

os.remove(CSV_PATH)
