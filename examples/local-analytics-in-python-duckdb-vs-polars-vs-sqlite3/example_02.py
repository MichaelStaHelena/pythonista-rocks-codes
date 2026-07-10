import csv
import sqlite3
import time

CSV_PATH = "/tmp/sales_1m.csv"
DB_PATH  = "/tmp/sales.db"

# ── 1. Connect with analytics-optimised pragmas ──────────────────────────────
# Python 3.12+ accepts autocommit=True (PEP 249v3 compliance).
# On older interpreters fall back to isolation_level=None.
import sys
if sys.version_info >= (3, 12):
    con = sqlite3.connect(DB_PATH, autocommit=True)
else:
    con = sqlite3.connect(DB_PATH, isolation_level=None)

con.execute("PRAGMA journal_mode = WAL")
con.execute("PRAGMA cache_size   = -65536")   # 64 MiB page cache
con.execute("PRAGMA synchronous  = NORMAL")

con.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        order_id         INTEGER PRIMARY KEY,
        region           TEXT    NOT NULL,
        product_category TEXT    NOT NULL,
        sale_amount      REAL    NOT NULL,   -- REAL enforces numeric affinity
        sale_date        TEXT    NOT NULL
    )
""")

# ── 2. Load: bulk insert via executemany ─────────────────────────────────────
t_load = time.perf_counter()
with open(CSV_PATH, newline="") as f:
    reader = csv.DictReader(f)
    rows = [
        (int(r["order_id"]), r["region"], r["product_category"],
         float(r["sale_amount"]), r["sale_date"])
        for r in reader
    ]
con.executemany(
    "INSERT OR IGNORE INTO sales VALUES (?,?,?,?,?)", rows
)
load_elapsed = time.perf_counter() - t_load
print(f"sqlite3 load : {load_elapsed:.2f}s")   # => ...

# ── 3. Filter + project ───────────────────────────────────────────────────────
t_filter = time.perf_counter()
cur = con.execute("""
    SELECT order_id, region, sale_amount
    FROM   sales
    WHERE  sale_amount > 500
      AND  region = 'North'
""")
filter_rows = cur.fetchall()
filter_elapsed = time.perf_counter() - t_filter
print(f"sqlite3 filter rows : {len(filter_rows):,}")   # => ...
print(f"sqlite3 filter time : {filter_elapsed:.3f}s")  # => ...

# ── 4. GroupBy + aggregation ──────────────────────────────────────────────────
t_agg = time.perf_counter()
cur = con.execute("""
    SELECT   region,
             product_category,
             SUM(sale_amount)   AS total_sales,
             COUNT(*)           AS order_count,
             AVG(sale_amount)   AS avg_sale
    FROM     sales
    GROUP BY region, product_category
    ORDER BY region, product_category
""")
agg_rows = cur.fetchall()
agg_elapsed = time.perf_counter() - t_agg
print(f"sqlite3 groupby rows : {len(agg_rows)}")       # => 500
print(f"sqlite3 groupby time : {agg_elapsed:.3f}s")    # => ...

con.close()
