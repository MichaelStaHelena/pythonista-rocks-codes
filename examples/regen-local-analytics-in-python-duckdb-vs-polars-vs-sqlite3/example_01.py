import sqlite3, csv, time, random, os, sys

random.seed(42)
N = 20_000
CSV_PATH = "trips.csv"

# Generate a synthetic trips dataset
with open(CSV_PATH, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["pickup_hour", "passenger_count", "trip_distance", "total_amount"])
    for _ in range(N):
        w.writerow([
            random.randint(0, 23),
            random.randint(0, 4),            # 0 = empty cab (later filtered out)
            round(random.uniform(0.5, 20.0), 2),
            round(random.uniform(3.0, 80.0), 2),
        ])

# ── Load phase: Python reads CSV row-by-row, then executemany sends to SQLite ──
t0 = time.perf_counter()
con = sqlite3.connect(":memory:")
con.execute("""
    CREATE TABLE trips (
        pickup_hour     INTEGER,
        passenger_count INTEGER,
        trip_distance   REAL,
        total_amount    REAL
    )
""")
with open(CSV_PATH) as f:
    reader = csv.DictReader(f)
    con.executemany(
        "INSERT INTO trips VALUES (:pickup_hour, :passenger_count, "
        ":trip_distance, :total_amount)",
        reader,
    )
con.commit()
load_ms = (time.perf_counter() - t0) * 1000

# ── Query phase: single-threaded SQLite VDBE, row-at-a-time execution ──────────
t1 = time.perf_counter()
rows = con.execute("""
    SELECT
        pickup_hour,
        COUNT(*)                        AS trip_count,
        ROUND(AVG(trip_distance), 4)    AS avg_distance,
        ROUND(SUM(total_amount),  2)    AS total_revenue
    FROM  trips
    WHERE passenger_count > 0
    GROUP BY pickup_hour
    ORDER BY pickup_hour
""").fetchall()
query_ms = (time.perf_counter() - t1) * 1000

print(f"Engine : sqlite3 {sqlite3.sqlite_version}  (Python {sys.version_info.major}.{sys.version_info.minor})")  # => Engine : sqlite3 3.53.1  (Python 3.13)
print(f"Rows   : {N:,}")                                                                                          # => Rows   : 20,000
print(f"Load   : {load_ms:.1f} ms  (Python CSV loop → executemany)")                                             # => ...
print(f"Query  : {query_ms:.1f} ms  (single-threaded VDBE)")                                                     # => ...
print(f"Groups : {len(rows)}")                                                                                    # => Groups : 24
print(f"Sample : hour={rows[0][0]}, trips={rows[0][1]}, "
      f"avg_dist={rows[0][2]}, revenue={rows[0][3]}")                                                            # => Sample : hour=0, trips=615, avg_dist=10.14, revenue=25528.89

os.remove(CSV_PATH)
