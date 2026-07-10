import pandas as pd

data = {
    "city":  ["Berlin", "Paris", "Berlin", "Paris", "Berlin"],
    "temp":  [12.1, 18.3, 10.5, 17.9, 13.4],
    "humid": [80, 65, 85, 60, 78],
}
df = pd.DataFrame(data)

print("pandas shape:", df.shape)           # => pandas shape: (5, 3)
print("pandas columns:", list(df.columns)) # => pandas columns: ['city', 'temp', 'humid']

# Boolean-mask filter — always call .copy() on slices you plan to modify
cold = df[df["temp"] < 13].copy()
print("cold rows:", len(cold))             # => cold rows: 2

# groupby + aggregation
avg = df.groupby("city")["temp"].mean().round(2)
print("Berlin avg temp:", avg["Berlin"])   # => Berlin avg temp: 12.0
print("Paris avg temp:", avg["Paris"])     # => Paris avg temp: 18.1

# ⚠️ pandas 3.0 Copy-on-Write (CoW) is ON by default: modifying a copy
# never silently modifies the original DataFrame.
df2 = df[df["city"] == "Berlin"].copy()
df2["temp"] = 0
print("original Berlin temp[0]:", df.loc[df["city"] == "Berlin", "temp"].iloc[0])
# => original Berlin temp[0]: 12.1
