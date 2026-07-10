# Save this file as test_examples.py and run: pytest test_examples.py -v
# ⚠️ Naming rules: file must start with test_  AND each function must start with test_
#    Pytest silently skips anything that doesn't match — it won't warn you.

import pytest
import requests
from unittest.mock import MagicMock
from pydantic import BaseModel, ValidationError


def add(a: int, b: int) -> int:
    return a + b


# Plain assert — pytest rewrites it to show a rich diff on failure.
# This magic only works with bare assert, NOT with assertEqual().
def test_add_positive():
    assert add(2, 3) == 5

def test_add_zero():
    assert add(0, 0) == 0


# parametrize: one test function drives multiple input/output pairs
@pytest.mark.parametrize("a,b,expected", [
    (1,  1,  2),
    (10, -3, 7),
    (0,  0,  0),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected


# fixture: reusable setup injected by name into any test that declares it
class User(BaseModel):
    name: str
    age: int

@pytest.fixture
def valid_user():
    return {"name": "Alice", "age": 30}

def test_user_model(valid_user):
    u = User(**valid_user)
    assert u.name == "Alice"
    assert u.age  == 30

def test_user_bad_age():
    with pytest.raises(ValidationError):
        User(name="Bob", age="not-a-number")  # type: ignore


# monkeypatch: replace requests.get without touching the network
def get_status(url: str) -> int:
    return requests.get(url, timeout=10).status_code

def test_get_status_mocked(monkeypatch):
    mock = MagicMock()
    mock.status_code = 200
    monkeypatch.setattr(requests, "get", lambda *a, **kw: mock)
    assert get_status("https://example.com") == 200
