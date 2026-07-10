import polars as pl
import time

CSV_PATH = "/tmp/sales_1m.csv"

# ── Eager: full materialisation ───────────────────────────────────────────────
t0 = time.perf_counter()
df_eager = pl.read_csv(CSV_PATH)
eager_load = time.perf_counter() - t0
print(f"Polars eager load  : {eager_load:.3f}s")     # => ...
print(f"Shape              : {df_eager.shape}")       # => ...

# ── Lazy: scan_csv builds a logical plan; nothing is read yet ─────────────────
# The optimizer applies predicate pushdown (filter before deserialising rows)
# and projection pushdown (skip unneeded columns at the scan level).
t0 = time.perf_counter()
result_lazy = (
    pl.scan_csv(CSV_PATH)
    .filter(
        (pl.col("sale_amount") > 500) & (pl.col("region") == "North")
    )
    .select(["order_id", "region", "sale_amount"])
    .collect()   # triggers optimisation + execution
)
lazy_filter = time.perf_counter() - t0
print(f"Polars lazy filter : {lazy_filter:.3f}s")    # => ...
print(f"Filter rows        : {len(result_lazy):,}")  # => ...

# ── Inspect the optimised logical plan before collecting ──────────────────────
lf = (
    pl.scan_csv(CSV_PATH)
    .filter(pl.col("sale_amount") > 500)
    .select(["region", "product_category", "sale_amount"])
)
print("\n── Optimised plan ──")                        # => ── Optimised plan ──
print(lf.explain(optimized=True))                      # => ...
