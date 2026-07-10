from pydantic import BaseModel, ValidationError
from typing import Optional

class Joke(BaseModel):
    id: Optional[int] = None
    setup: str            # required — pydantic enforces this at instantiation
    punchline: str        # required

# --- happy path ---
j = Joke(setup="Why did the dev quit?", punchline="No exceptions.")
print("pydantic setup:", j.setup)            # => pydantic setup: Why did the dev quit?
# ⚠️ v1 gotcha: .dict() was removed in v2 — use .model_dump() instead
print("pydantic model_dump:", j.model_dump())
# => pydantic model_dump: {'id': None, 'setup': 'Why did the dev quit?', 'punchline': 'No exceptions.'}

# --- bad data: missing required field raises ValidationError immediately ---
try:
    Joke(punchline="No setup here")
except ValidationError as exc:
    errors = exc.errors()
    print("validation field:", errors[0]["loc"][0])   # => validation field: setup
    print("validation type:", errors[0]["type"])       # => validation type: missing
