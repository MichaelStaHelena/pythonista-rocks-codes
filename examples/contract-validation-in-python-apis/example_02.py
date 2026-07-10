from pydantic import BaseModel, field_validator, model_validator, ValidationError, ConfigDict
from typing import Optional

class OrderRequest(BaseModel):
    item_id: str
    quantity: int
    unit_price: float
    discount_pct: float = 0.0
    coupon: Optional[str] = None

    @field_validator("unit_price", mode="after")
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("unit_price must be greater than zero")
        return v

    @model_validator(mode="after")
    def discount_cannot_exceed_price(self) -> "OrderRequest":
        if self.discount_pct >= self.unit_price:
            raise ValueError(
                f"discount_pct ({self.discount_pct}) must be less than "
                f"unit_price ({self.unit_price})"
            )
        return self   # ← required; omitting this makes model_validate() return None

# Valid order
order = OrderRequest(item_id="SKU-1", quantity=2, unit_price=19.99, discount_pct=5.00)
print(order.discount_pct)   # => 5.0

# Cross-field violation
try:
    OrderRequest(item_id="SKU-3", quantity=1, unit_price=10.00, discount_pct=15.00)
except ValidationError as exc:
    errors = exc.errors()
    print(len(errors))           # => 1
    print(errors[0]["loc"])      # => ()
    print(errors[0]["msg"])      # => Value error, discount_pct (15.0) must be less than unit_price (10.0)

# ── The return-self trap (GitHub issue #9334) ─────────────────────────────────
# If @model_validator(mode='after') forgets `return self`:
#   model_validate({...})  → returns None, no exception raised
#   ModelClass(**kwargs)   → still works, masking the bug in keyword-arg tests

class BrokenOrderRequest(BaseModel):
    item_id: str
    unit_price: float
    discount_pct: float = 0.0

    @model_validator(mode="after")
    def discount_cannot_exceed_price(self) -> "BrokenOrderRequest":
        if self.discount_pct >= self.unit_price:
            raise ValueError("discount_pct must be less than unit_price")
        # ← forgot return self

via_validate = BrokenOrderRequest.model_validate(
    {"item_id": "SKU-4", "unit_price": 20.0, "discount_pct": 3.0}
)
print(via_validate)                    # => None  ← silent data loss

via_kwargs = BrokenOrderRequest(item_id="SKU-4", unit_price=20.0, discount_pct=3.0)
print(type(via_kwargs).__name__)       # => BrokenOrderRequest  ← masks the bug in tests

# ── Strict mode: reject silent coercion at the boundary ──────────────────────
# By default, pydantic accepts "3" for an int field (lax mode).
# Set strict=True so the contract means what it says.

class StrictOrder(BaseModel):
    model_config = ConfigDict(strict=True)
    quantity: int

try:
    StrictOrder.model_validate({"quantity": "3"})   # string rejected for int
except ValidationError as exc:
    print(exc.errors()[0]["msg"])   # => Input should be a valid integer
