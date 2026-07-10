import polars as pl

CSV_PATH = "/tmp/sales_1m.csv"

lf = pl.scan_csv(CSV_PATH)

# collect_schema() is the canonical v1.x API for LazyFrame schema inspection.
# Calling .schema on a LazyFrame is still available but emits a deprecation
# warning in Polars 1.x to encourage use of collect_schema() instead.
schema = lf.collect_schema()
print("Columns:", schema.names())    # => Columns: ['order_id', 'region', 'product_category', 'sale_amount', 'sale_date']
print("Dtypes :", schema.dtypes())   # => ...

# GroupBy aggregation — group_by makes NO ordering guarantee.
# Always add .sort() if deterministic output is required.
result = (
    lf.group_by(["region", "product_category"])
    .agg(
        pl.col("sale_amount").sum().alias("total_sales"),
        pl.len().alias("order_count"),
        pl.col("sale_amount").mean().alias("avg_sale"),
    )
    .sort(["region", "product_category"])   # explicit sort: group_by is unordered
    .collect()
)
print(f"GroupBy rows : {len(result)}")     # => GroupBy rows : 500
print(result.head(3))                      # => ...
