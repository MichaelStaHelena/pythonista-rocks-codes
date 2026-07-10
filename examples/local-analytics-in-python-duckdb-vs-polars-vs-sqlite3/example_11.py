import duckdb
import threading
import time

CSV_PATH = "/tmp/sales_1m.csv"
results  = {}

def query_worker(thread_id: int) -> None:
    # Each thread opens its own connection — no cross-thread lock contention.
    # Sharing a single connection across threads forces serialisation inside DuckDB.
    con = duckdb.connect()
    con.execute(f"CREATE VIEW sales AS SELECT * FROM read_csv_auto('{CSV_PATH}')")
    t0  = time.perf_counter()
    row = con.execute(
        "SELECT COUNT(*) FROM sales WHERE sale_amount > 500"
    ).fetchone()
    results[thread_id] = (row[0], time.perf_counter() - t0)
    con.close()

threads = [threading.Thread(target=query_worker, args=(i,)) for i in range(3)]
for t in threads: t.start()
for t in threads: t.join()

for tid, (count, elapsed) in sorted(results.items()):
    print(f"Thread {tid}: {count:,} rows in {elapsed:.3f}s")   # => ...
