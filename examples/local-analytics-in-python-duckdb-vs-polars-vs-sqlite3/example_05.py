import duckdb
import pyarrow as pa

# Build a small Arrow table — no pandas, no serialisation round-trip.
arrow_table = pa.table({
    "region":           ["North", "South", "East",  "North", "South"],
    "product_category": ["Cat_01","Cat_02","Cat_01","Cat_03","Cat_01"],
    "sale_amount":      [120.5,   340.0,   890.0,   450.0,  610.0],
})

con = duckdb.connect()
# Register the Arrow table as a virtual DuckDB relation.
# No copy occurs: DuckDB reads directly from the Arrow buffer.
con.register("arrow_sales", arrow_table)

result = con.execute("""
    SELECT   region,
             SUM(sale_amount)  AS total,
             COUNT(*)          AS n
    FROM     arrow_sales
    GROUP BY region
    ORDER BY region
""").arrow()   # Result returned as an Arrow table — still no Python-tuple allocation.

print(type(result).__name__)                         # => Table
print(result.schema)                                 # => ...
print(result.to_pydict())                            # => ...
con.close()
