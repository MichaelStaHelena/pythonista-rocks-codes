from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional

class User(BaseModel):
    # V2 config: model_config = ConfigDict(...)  NOT  class Config:
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    age: int
    email: Optional[str] = None

    # V2 validator: @field_validator, NOT @validator
    @field_validator("age")
    @classmethod
    def age_must_be_positive(cls, v: int) -> int:
        if v < 0:
            raise ValueError("age must be non-negative")
        return v

alice = User(name="  Alice  ", age=30, email="alice@example.com")
print("name:", alice.name)          # => name: Alice     (whitespace stripped)
print("age:", alice.age)            # => age: 30

# ✗ GOTCHA: model.dict() is V1 — use model.model_dump() in V2
data = alice.model_dump()
print("keys:", sorted(data.keys()))  # => keys: ['age', 'email', 'name']
print("email:", data["email"])       # => email: alice@example.com

# Validation errors are rich and precise
from pydantic import ValidationError
try:
    User(name="Bob", age=-5)
except ValidationError as e:
    msgs = [err["msg"] for err in e.errors()]
    print("validation error:", msgs[0])   # => validation error: Value error, age must be non-negative
