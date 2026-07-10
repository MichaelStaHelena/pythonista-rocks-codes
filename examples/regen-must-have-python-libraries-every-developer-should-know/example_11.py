# test_fetch_users.py  ← must start with test_ for pytest to find it
# Run:  pytest test_fetch_users.py -v

import pytest
from pydantic import ValidationError
from fetch_users import User

def test_user_valid():
    u = User(id=1, name="Alice", username="alice", email="a@example.com")
    assert u.name == "Alice"
    assert u.id == 1

def test_user_rejects_missing_email():
    with pytest.raises(ValidationError):
        User(id=2, name="Bob", username="bob")   # email is required

def test_user_rejects_wrong_type():
    with pytest.raises(ValidationError):
        User(id="not-an-int", name="Carol", username="carol", email="c@example.com")

# pytest 9 subtests: all cases run even if one fails
def test_user_name_variations(subtests):
    names = ["Alice", "Böb", "张伟", "O'Brien"]
    for name in names:
        with subtests.test(msg=name):
            u = User(id=1, name=name, username="u", email="x@x.com")
            assert u.name == name
