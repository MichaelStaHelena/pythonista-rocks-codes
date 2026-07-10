import sqlite3, duckdb, polars as pl, csv, os

CSV_PATH = "events.csv"

rows = [
    ("2024-03-01 08:15:00", "A", 12.5),
    ("2024-03-01 14:22:00", "B",  7.0),
    ("2024-03-02 09:05:00", "A", 19.3),
    ("2024-03-02 22:47:00", "B",  4.8),
    ("2024-03-03 11:30:00", "A",  8.1),
]
with open(CSV_PATH, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["event_time", "category", "value"])
    w.writerows(rows)

# ── sqlite3: datetimes are TEXT; date arithmetic requires strftime() ───────────
# SQLite has no DATETIME column type — it uses "type affinity" and stores the
# ISO string verbatim. Temporal math is delegated entirely to strftime().
con_sq = sqlite3.connect(":memory:")
con_sq.execute("CREATE TABLE events (event_time TEXT, category TEXT, value REAL)")
con_sq.executemany("INSERT INTO events VALUES (?,?,?)", rows)

sq_result = con_sq.execute("""
    SELECT category,
           strftime('%Y-%m-%d', event_time) AS day,
           ROUND(SUM(value), 2)             AS total
    FROM   events
    GROUP  BY category, strftime('%Y-%m-%d', event_time)
    ORDER  BY day, category
""").fetchall()

print("sqlite3  | type stored : TEXT (no native TIMESTAMP)")                   # => sqlite3  | type stored : TEXT (no native TIMESTAMP)
print("sqlite3  | result      :", sq_result)                                   # => sqlite3  | result      : [('A', '2024-03-01', 12.5), ('B', '2024-03-01', 7.0), ('A', '2024-03-02', 19.3), ('B', '2024-03-02', 4.8), ('A', '2024-03-03', 8.1)]

# ── DuckDB: TIMESTAMP inferred by read_csv_auto; ::DATE cast is native ─────────
con_dk = duckdb.connect()
con_dk.execute("SET threads=2; SET memory_limit='512MB'")
dk_result = con_dk.execute("""
    SELECT category,
           event_time::DATE          AS day,
           ROUND(SUM(value), 2)      AS total
    FROM   read_csv_auto('events.csv')
    GROUP  BY category, event_time::DATE
    ORDER  BY day, category
""").fetchall()

print("\nduckdb   | type inferred: TIMESTAMP (native temporal arithmetic)")     # => ...
print("duckdb   | result       :", dk_result)                                  # => duckdb   | result       : [('A', datetime.date(2024, 3, 1), 12.5), ('B', datetime.date(2024, 3, 1), 7.0), ('A', datetime.date(2024, 3, 2), 19.3), ('B', datetime.date(2024, 3, 2), 4.8), ('A', datetime.date(2024, 3, 3), 8.1)]

# ── Polars: explicit parse to pl.Datetime, then .dt accessor for date parts ────
pl_result = (
    pl.scan_csv(CSV_PATH, schema_overrides={"event_time": pl.String})
      .with_columns(
          pl.col("event_time")
            .str.to_datetime("%Y-%m-%d %H:%M:%S")
            .alias("event_time")
      )
      .with_columns(pl.col("event_time").dt.date().alias("day"))
      .group_by(["category", "day"])
      .agg(pl.col("value").sum().round(2).alias("total"))
      .sort(["day", "category"])
      .collect()
)

print("\npolars   | type used    : pl.Datetime → .dt.date()")  # => ...
print("polars   | result       :")                             # => polars   | result       :
print(pl_result)                                              # => ...

os.remove(CSV_PATH)
