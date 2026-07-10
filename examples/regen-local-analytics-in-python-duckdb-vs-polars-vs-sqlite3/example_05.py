import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "pyarrow", "-q"], check=True)

import duckdb, polars as pl, csv, random, os

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

con = duckdb.connect()
con.execute("SET threads = 2; SET memory_limit = '512MB'")

# Step 1 — DuckDB aggregates; .arrow() exports as a pyarrow.RecordBatchReader.
# The columnar buffers are shared, not copied, because both DuckDB and PyArrow
# speak the Arrow C Data Interface (PEP 711 / Arrow spec).
arrow_table = con.execute("""
    SELECT
        pickup_hour,
        COUNT(*)                        AS trip_count,
        ROUND(AVG(trip_distance), 4)    AS avg_distance,
        ROUND(SUM(total_amount),  2)    AS total_revenue
    FROM  read_csv_auto('trips.csv')
    WHERE passenger_count > 0
    GROUP BY pickup_hour
    ORDER BY pickup_hour
""").arrow()

print(f"Arrow table : {type(arrow_table).__module__}.{type(arrow_table).__name__}")  # => Arrow table : pyarrow.lib.RecordBatchReader
print(f"Schema      : {arrow_table.schema}")                                          # => ...

# Step 2 — pl.from_arrow() wraps the Arrow buffers without an additional memcpy.
df = pl.from_arrow(arrow_table)

# Step 3 — Polars-native post-processing unavailable in SQL: revenue share per hour.
df = df.with_columns(
    (pl.col("total_revenue") / pl.col("total_revenue").sum() * 100)
    .round(2)
    .alias("revenue_pct")
)

print(f"\nPolars frame : {type(df).__name__}, schema={df.schema}")  # => ...
print(f"\nTop 5 hours by revenue share:")                           # => ...
print(df.sort("revenue_pct", descending=True).head(5))             # => ...

os.remove(CSV_PATH)
