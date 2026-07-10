import sqlite3

# SQLite stores everything as TEXT when no affinity is declared,
# then compares lexicographically — '9' > '500' is True, '1500' < '500' is False.
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE bad (amount TEXT)")          # TEXT affinity — wrong for numerics
con.execute("CREATE TABLE good (amount REAL)")         # REAL affinity — correct

con.executemany("INSERT INTO bad  VALUES (?)", [("9.99",), ("150.00",), ("1500.00",)])
con.executemany("INSERT INTO good VALUES (?)", [(9.99,),  (150.00,),   (1500.00,)])

# TEXT column: '9.99' > '500' is True (lexicographic), '1500.00' < '500' is True (!)
bad_rows  = con.execute("SELECT amount FROM bad  WHERE amount > '500'").fetchall()
good_rows = con.execute("SELECT amount FROM good WHERE amount > 500").fetchall()

print("TEXT affinity (wrong):", [r[0] for r in bad_rows])   # => TEXT affinity (wrong): ['9.99', '1500.00']
print("REAL affinity (correct):", [r[0] for r in good_rows]) # => REAL affinity (correct): [1500.0]
con.close()
