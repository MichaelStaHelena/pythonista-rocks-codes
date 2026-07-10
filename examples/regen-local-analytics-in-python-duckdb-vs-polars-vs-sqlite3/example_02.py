import duckdb, csv, time, random, os

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
# Explicitly cap threads and memory — critical on shared or CI machines
# where os.cpu_count() would otherwise claim every core.
con.execute("SET threads = 2; SET memory_limit = '512MB'")

# No explicit load step: DuckDB sniffs schema and reads the file inside the query.
# The vectorized execution engine processes columnar chunks of 2 048 values at a time,
# applying the WHERE filter as a selection vector before any aggregation work occurs.
t1 = time.perf_counter()
rows = con.execute("""
    SELECT
        pickup_hour,
        COUNT(*)                        AS trip_count,
        ROUND(AVG(trip_distance), 4)    AS avg_distance,
        ROUND(SUM(total_amount),  2)    AS total_revenue
    FROM  read_csv_auto('trips.csv')
    WHERE passenger_count > 0
    GROUP BY pickup_hour
    ORDER BY pickup_hour
""").fetchall()
query_ms = (time.perf_counter() - t1) * 1000

print(f"Engine : duckdb {duckdb.__version__}")                               # => Engine : duckdb 1.5.4
print(f"Rows   : {N:,}")                                                     # => Rows   : 20,000
print(f"Load   : n/a — file scanned inline (no pre-load step)")              # => Load   : n/a — file scanned inline (no pre-load step)
print(f"Query  : {query_ms:.1f} ms  (vectorized, 2 threads, incl. CSV parse)")  # => ...
print(f"Groups : {len(rows)}")                                               # => Groups : 24
print(f"Sample : hour={rows[0][0]}, trips={rows[0][1]}, "
      f"avg_dist={float(rows[0][2]):.4f}, revenue={float(rows[0][3]):.2f}") # => Sample : hour=0, trips=615, avg_dist=10.1400, revenue=25528.89

os.remove(CSV_PATH)
