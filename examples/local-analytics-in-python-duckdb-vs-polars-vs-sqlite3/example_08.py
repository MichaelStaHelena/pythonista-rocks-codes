import polars as pl

CSV_PATH = "/tmp/sales_1m.csv"

# .collect(engine="streaming") processes data in bounded batches,
# allowing datasets larger than RAM to be processed.
# Not all operations are streaming-safe; the engine falls back silently
# for unsupported nodes. Use .explain(engine="streaming") to confirm.

lf = (
    pl.scan_csv(CSV_PATH)
    .filter(pl.col("sale_amount") > 500)
    .group_by(["region", "product_category"])
    .agg(pl.col("sale_amount").sum().alias("total_sales"))
    .sort(["region", "product_category"])
)

# Inspect whether the streaming engine will be used end-to-end.
print("── Streaming plan ──")                          # => ── Streaming plan ──
print(lf.explain(engine="streaming"))                  # => ...

result = lf.collect(engine="streaming")
print(f"Streaming result rows : {len(result)}")        # => ...
