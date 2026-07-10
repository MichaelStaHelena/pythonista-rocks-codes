# pip install requests python-dotenv pydantic pandas loguru rich
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock
from typing import Optional

from dotenv import load_dotenv
import requests
from pydantic import BaseModel, ValidationError
import pandas as pd
from loguru import logger
from rich.console import Console
from rich.table import Table

# ── 1. python-dotenv: load the API key before anything else ──────────────────
# In a real project this would be a .env file you've git-ignored.
with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
    f.write("JOKES_API_KEY=demo-key-xyz\n")
    env_path = f.name

load_dotenv(dotenv_path=env_path, override=True)
api_key = os.getenv("JOKES_API_KEY")

# ── 2. loguru: configure once at the top of your entry point ─────────────────
logger.remove()
logger.add(sys.stdout, format="{level}: {message}", colorize=False)
logger.info(f"API key loaded: {api_key}")

# ── 3. pydantic: define the shape of a valid joke record ─────────────────────
class JokeRecord(BaseModel):
    id: Optional[int] = None
    setup: str
    punchline: str
    joke_type: Optional[str] = None

# ── 4. requests: fetch jokes (mocked here so no network is needed) ────────────
RAW_JOKES = [
    {"id": 1, "type": "general",     "setup": "Why do Java devs wear glasses?",    "punchline": "Because they don't C#."},
    {"id": 2, "type": "general",     "setup": "How do you comfort a JS bug?",      "punchline": "You console it."},
    {"id": 3, "type": "knock-knock", "setup": "Knock knock. Who's there? Recursion.", "punchline": "Knock knock..."},
]

jokes: list[JokeRecord] = []
for raw in RAW_JOKES:
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = raw

    with patch("requests.get", return_value=mock_resp):
        r = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=10)
        r.raise_for_status()                        # always guard against 4xx/5xx
        data = r.json()

    try:
        jokes.append(JokeRecord(
            id=data.get("id"),
            setup=data["setup"],
            punchline=data["punchline"],
            joke_type=data.get("type"),
        ))
    except ValidationError as exc:
        logger.warning(f"skipping invalid record: {exc}")

logger.info(f"fetched {len(jokes)} jokes")

# ── 5. pandas: analyse the data ──────────────────────────────────────────────
df = pd.DataFrame([j.model_dump() for j in jokes])
counts = df.groupby("joke_type")["id"].count().sort_index()
logger.info("groupby complete")

# ── 6. rich: print a formatted summary table ─────────────────────────────────
console = Console(highlight=False, no_color=True)
tbl = Table(title="Joke Type Summary")
tbl.add_column("Type")
tbl.add_column("Count", justify="right")
for jtype, cnt in counts.items():
    tbl.add_row(str(jtype), str(cnt))
console.print(tbl)

os.unlink(env_path)
