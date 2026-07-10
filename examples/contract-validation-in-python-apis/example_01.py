from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional

class OrderRequest(BaseModel):
    item_id: str
    quantity: int
    unit_price: float
    coupon: Optional[str] = None   # v2 requires the explicit = None

    @field_validator("unit_price", mode="after")
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("unit_price must be greater than zero")
        return v

# Valid payload
order = OrderRequest(item_id="SKU-1", quantity=3, unit_price=9.99)
print(order.item_id)   # => SKU-1
print(order.coupon)    # => None

# Invalid payload — ValidationError carries a structured .errors() list
try:
    OrderRequest(item_id="SKU-2", quantity=1, unit_price=-5.00)
except ValidationError as exc:
    errors = exc.errors()
    print(len(errors))          # => 1
    print(errors[0]["loc"])     # => ('unit_price',)
    print(errors[0]["msg"])     # => Value error, unit_price must be greater than zero
    print(errors[0]["type"])    # => value_error

# ── The Optional[T] gotcha ────────────────────────────────────────────────────
# v1 behaviour:  Optional[str]      → not required, defaults to None
# v2 behaviour:  Optional[str]      → REQUIRED, just also accepts None
#                Optional[str] = None → not required, defaults to None

class BrokenModel(BaseModel):
    note: Optional[str]          # required in v2 — raises if omitted

class FixedModel(BaseModel):
    note: Optional[str] = None   # not required, defaults to None

try:
    BrokenModel()
except ValidationError as exc:
    print(exc.errors()[0]["msg"])   # => Field required

fixed = FixedModel()
print(fixed.note)                   # => None
