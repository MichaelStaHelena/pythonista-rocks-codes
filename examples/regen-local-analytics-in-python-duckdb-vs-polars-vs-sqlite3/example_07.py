import polars as pl

df = pl.DataFrame({
    "city":  ["Berlin", "Athens", "Cairo", "Berlin", "Athens", "Cairo"],
    "sales": [100, 200, 150, 80, 90, 60],
})

# group_by output order is undefined — Polars uses a parallel hash-table
# whose bucket iteration order is not guaranteed across runs or versions.
unordered = df.group_by("city").agg(pl.col("sales").sum())
print("group_by (no sort guarantee):")  # => group_by (no sort guarantee):
print(unordered)                        # => ...

# Remedy 1: explicit .sort() after aggregation — safest and most explicit
ordered_a = (
    df.group_by("city")
      .agg(pl.col("sales").sum())
      .sort("city")
)
print("\ngroup_by + explicit .sort('city'):")  # => ...
print(ordered_a)                              # => ...

# Remedy 2: maintain_order=True preserves the first-seen insertion order
# (deterministic but not alphabetical; has a small performance cost)
ordered_b = df.group_by("city", maintain_order=True).agg(pl.col("sales").sum())
print("\ngroup_by(maintain_order=True) — preserves first-seen order:")  # => ...
print(ordered_b)                                                        # => ...
