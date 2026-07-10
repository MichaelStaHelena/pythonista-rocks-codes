import duckdb
import time

CSV_PATH = "/tmp/sales_1m.csv"

# duckdb.connect() with no path → in-memory, ephemeral, fastest for one-shot analytics.
# duckdb.connect("my.duckdb") → persisted columnar file.
con = duckdb.connect()

# ── 1. Load: register CSV as a view (no materialisation yet) ─────────────────
# DuckDB's parallel CSV reader (PR #5194) uses all available cores automatically.
t_load = time.perf_counter()
con.execute(f"CREATE VIEW sales AS SELECT * FROM read_csv_auto('{CSV_PATH}')")
load_elapsed = time.perf_counter() - t_load
print(f"DuckDB view create : {load_elapsed:.4f}s")   # => ...

# ── 2. Filter + project ───────────────────────────────────────────────────────
t_filter = time.perf_counter()
filter_rel = con.execute("""
    SELECT order_id, region, sale_amount
    FROM   sales
    WHERE  sale_amount > 500
      AND  region = 'North'
""")
filter_rows = filter_rel.fetchall()
filter_elapsed = time.perf_counter() - t_filter
print(f"DuckDB filter rows : {len(filter_rows):,}")    # => ...
print(f"DuckDB filter time : {filter_elapsed:.3f}s")   # => ...

# ── 3. GroupBy + aggregation ──────────────────────────────────────────────────
t_agg = time.perf_counter()
agg_rel = con.execute("""
    SELECT   region,
             product_category,
             SUM(sale_amount)   AS total_sales,
             COUNT(*)           AS order_count,
             AVG(sale_amount)   AS avg_sale
    FROM     sales
    GROUP BY region, product_category
    ORDER BY region, product_category
""")
agg_rows = agg_rel.fetchall()
agg_elapsed = time.perf_counter() - t_agg
print(f"DuckDB groupby rows : {len(agg_rows)}")        # => 500
print(f"DuckDB groupby time : {agg_elapsed:.3f}s")     # => ...

# ── 4. EXPLAIN ANALYZE: inspect the physical operator tree ───────────────────
# EXPLAIN ANALYZE executes the query and annotates each operator with
# actual row counts and wall-clock time.
plan = con.execute("""
    EXPLAIN ANALYZE
    SELECT   region, SUM(sale_amount)
    FROM     sales
    WHERE    sale_amount > 500
    GROUP BY region
""").fetchall()
print("\n── EXPLAIN ANALYZE (first 6 lines) ──")      # => ── EXPLAIN ANALYZE (first 6 lines) ──
for row in plan[:6]:
    print(row[1])                                      # => ...

con.close()
