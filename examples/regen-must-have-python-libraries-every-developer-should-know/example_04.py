import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Carol"],
    "score": [88, 72, 95],
})

# ✗ GOTCHA (pandas 3.0+): chained assignment does nothing — CoW is on by default
df["score"][0] = 999          # no error, but the DataFrame is NOT changed
print("after chained assign:", df["score"].tolist())   # => after chained assign: [88, 72, 95]

# ✓ RIGHT: always use .loc for single-cell writes
df.loc[0, "score"] = 999
print("after .loc assign:", df["score"].tolist())      # => after .loc assign: [999, 72, 95]

# String dtype changed in pandas 3.0: columns are no longer object dtype
print("name dtype:", df["name"].dtype)    # => name dtype: object

# Filtering still works exactly as before
top = df[df["score"] > 80][["name", "score"]]
print(top.to_string(index=False))
# => name  score
# => Alice    999
# => Carol     95
