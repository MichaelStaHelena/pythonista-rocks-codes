import csv
import sqlite3
import time
import duckdb
import polars as pl

CSV_PATH = "/tmp/sales_1m.csv"
DB_PATH  = "/tmp/sales_timing.db"

QUERY_LABEL = "GroupBy: SUM/COUNT/AVG by region × category"

# ── sqlite3 ───────────────────────────────────────────────────────────────────
import sys
if sys.version_info >= (3, 12):
    con_sq = sqlite3.connect(DB_PATH, autocommit=True)
else:
    con_sq = sqlite3.connect(DB_PATH, isolation_level=None)
con_sq.execute("PRAGMA journal_mode = WAL")
con_sq.execute("PRAGMA cache_size   = -65536")
con_sq.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        order_id INTEGER, region TEXT, product_category TEXT,
        sale_amount REAL, sale_date TEXT
    )
""")
row_count = con_sq.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
if row_count == 0:
    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        rows = [(int(r["order_id"]), r["region"], r["product_category"],
                 float(r["sale_amount"]), r["sale_date"]) for r in reader]
    con_sq.executemany("INSERT INTO sales VALUES (?,?,?,?,?)", rows)

t0 = time.perf_counter()
con_sq.execute("""
    SELECT region, product_category,
           SUM(sale_amount), COUNT(*), AVG(sale_amount)
    FROM   sales
    GROUP BY region, product_category
""").fetchall()
sq_agg = time.perf_counter() - t0
con_sq.close()

# ── DuckDB ────────────────────────────────────────────────────────────────────
con_dk = duckdb.connect()
con_dk.execute(f"CREATE VIEW sales AS SELECT * FROM read_csv_auto('{CSV_PATH}')")

t0 = time.perf_counter()
con_dk.execute("""
    SELECT region, product_category,
           SUM(sale_amount), COUNT(*), AVG(sale_amount)
    FROM   sales
    GROUP BY region, product_category
""").fetchall()
dk_agg = time.perf_counter() - t0
con_dk.close()

# ── Polars lazy ───────────────────────────────────────────────────────────────
t0 = time.perf_counter()
(
    pl.scan_csv(CSV_PATH)
    .group_by(["region", "product_category"])
    .agg(
        pl.col("sale_amount").sum(),
        pl.len(),
        pl.col("sale_amount").mean(),
    )
    .collect()
)
pl_agg = time.perf_counter() - t0

# ── Print comparison table ────────────────────────────────────────────────────
print(f"{'Engine':<15} {'GroupBy time':>14}  {'vs sqlite3':>10}")
print("-" * 44)
print(f"{'sqlite3':<15} {sq_agg:>13.3f}s  {'1.0×':>10}")
print(f"{'duckdb':<15} {dk_agg:>13.3f}s  {sq_agg/dk_agg:>9.1f}×")
print(f"{'polars (lazy)':<15} {pl_agg:>13.3f}s  {sq_agg/pl_agg:>9.1f}×")
# => ...
