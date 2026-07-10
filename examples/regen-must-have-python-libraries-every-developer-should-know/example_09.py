# Save this file as test_math.py  ← MUST start with test_
# Then run:  pytest test_math.py -v

def add(a, b):
    return a + b

def test_add_integers():
    # ✓ Plain assert — pytest rewrites this to show a rich diff on failure
    assert add(2, 3) == 5

def test_add_strings():
    assert add("hello", " world") == "hello world"

def test_add_negative():
    assert add(-1, 1) == 0

# ✗ WRONG (unittest style — works but loses pytest's diff magic):
# import unittest
# class TestAdd(unittest.TestCase):
#     def test_add(self):
#         self.assertEqual(add(2, 3), 5)   # ← diffs are worse

# pytest 9+ native subtests — test multiple inputs without stopping at first failure
def test_add_many_inputs(subtests):
    cases = [(1, 2, 3), (0, 0, 0), (-5, 5, 0), (100, 200, 300)]
    for a, b, expected in cases:
        with subtests.test(msg=f"{a}+{b}", a=a, b=b):
            assert add(a, b) == expected
