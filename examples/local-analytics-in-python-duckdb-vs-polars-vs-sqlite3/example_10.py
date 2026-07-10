import polars as pl

# Demonstrate that group_by output order is non-deterministic.
# Use .sort() for reproducible output.
df = pl.DataFrame({
    "region": ["South", "North", "East", "North", "South", "East"],
    "amount": [100.0, 200.0, 150.0, 300.0, 50.0, 400.0],
})

unordered = df.group_by("region").agg(pl.col("amount").sum())
ordered   = df.group_by("region").agg(pl.col("amount").sum()).sort("region")

print("Unordered regions:", sorted(unordered["region"].to_list()))  # => Unordered regions: ['East', 'North', 'South']
print("Ordered regions  :", ordered["region"].to_list())            # => Ordered regions  : ['East', 'North', 'South']

# Polars 1.x dtype migration: pl.Utf8 resolves as an alias but pl.String is canonical.
# Code ported from 0.x should update all Utf8 references.
s = pl.Series(["a", "b", "c"], dtype=pl.String)
print(f"dtype        : {s.dtype}")           # => dtype        : String
print(f"pl.String is pl.Utf8 : {pl.String is pl.Utf8}")  # => pl.String is pl.Utf8 : True
