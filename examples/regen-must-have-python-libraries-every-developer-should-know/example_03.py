import numpy as np

# Basic array — dtype is inferred
a = np.array([1, 2, 3, 4, 5])
print("array:", a)          # => array: [1 2 3 4 5]
print("dtype:", a.dtype)    # => dtype: int64

# Vectorised math — no Python loop needed
print("squared:", a ** 2)   # => squared: [ 1  4  9 16 25]
print("mean:", a.mean())    # => mean: 3.0

# ✗ GOTCHA: inserting a float into an int array silently truncates
b = np.array([10, 20, 30], dtype=np.int64)
b[0] = 3.99          # 3.99 becomes 3 — no warning!
print("after b[0] = 3.99:", b)   # => after b[0] = 3.99: [ 3 20 30]

# ✓ RIGHT: declare float dtype when your data is float
c = np.array([10, 20, 30], dtype=np.float64)
c[0] = 3.99
print("after c[0] = 3.99:", c)   # => after c[0] = 3.99: [ 3.99 20.   30.  ]

# NumPy 2.x: old aliases are gone — use the underscore forms
print("bool_ :", np.bool_)        # => bool_ : <class 'numpy.bool_'>
print("int_  :", np.int_)         # => int_  : <class 'numpy.intp'>
print("float64:", np.float64)     # => float64: <class 'numpy.float64'>
