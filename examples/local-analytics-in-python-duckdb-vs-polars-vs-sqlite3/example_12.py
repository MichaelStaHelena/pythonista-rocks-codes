import sqlite3
import sys

# Python 3.12 added sqlite3.Connection.autocommit (PEP 249v3).
# Python 3.13 deprecated positional use of timeout/detect_types/etc in connect().
# For analytics workloads, autocommit eliminates the implicit deferred-transaction
# overhead that wraps every SELECT in the default mode.

print(f"Python version  : {sys.version_info.major}.{sys.version_info.minor}")  # => ...
print(f"SQLite version  : {sqlite3.sqlite_version}")                            # => ...

if sys.version_info >= (3, 12):
    con = sqlite3.connect(":memory:", autocommit=True)
    print(f"autocommit attr : {con.autocommit}")   # => autocommit attr : True
    con.close()
else:
    # Pre-3.12 idiom: isolation_level=None puts the connection in autocommit mode.
    con = sqlite3.connect(":memory:", isolation_level=None)
    print("isolation_level=None (legacy autocommit)")   # => isolation_level=None (legacy autocommit)
    con.close()
