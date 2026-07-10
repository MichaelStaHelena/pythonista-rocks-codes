import polars as pl
import csv, time, random, os

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

# scan_csv() returns a LazyFrame — zero bytes are read from disk at this point.
# Each chained call appends a node to the logical plan graph.
# .collect() hands the graph to the optimizer before invoking the Rust executor.
t1 = time.perf_counter()
result = (
    pl.scan_csv(CSV_PATH)                    # LazyFrame — no I/O yet
      .filter(pl.col("passenger_count") > 0) # predicate pushed down to the scan
      .group_by("pickup_hour")
      .agg(
          pl.len().alias("trip_count"),
          pl.col("trip_distance").mean().round(4).alias("avg_distance"),
          pl.col("total_amount").sum().round(2).alias("total_revenue"),
      )
      .sort("pickup_hour")
      .collect()                             # triggers optimizer + Rust execution
)
query_ms = (time.perf_counter() - t1) * 1000

print(f"Engine : polars {pl.__version__}")                                            # => Engine : polars 1.42.1
print(f"Rows   : {N:,}")                                                              # => Rows   : 20,000
print(f"Load   : n/a — scanned lazily via scan_csv (no pre-load step)")              # => Load   : n/a — scanned lazily via scan_csv (no pre-load step)
print(f"Query  : {query_ms:.1f} ms  (lazy plan, predicate pushdown, Rust core)")     # => ...
print(f"Groups : {len(result)}")                                                      # => Groups : 24
r = result.row(0)
print(f"Sample : hour={r[0]}, trips={r[1]}, avg_dist={r[2]}, revenue={r[3]}")       # => Sample : hour=0, trips=615, avg_dist=10.14, revenue=25528.89

os.remove(CSV_PATH)
