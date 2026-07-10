# fetch_users.py
# pip install httpx pydantic loguru rich python-dotenv
# Create a .env file with:  BASE_URL=https://jsonplaceholder.typicode.com

import asyncio
import os
import sys

from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel, ValidationError
from rich.console import Console
from rich.table import Table
import httpx

# ── Config ──────────────────────────────────────────────────────────────────
load_dotenv()                                   # reads .env into os.environ
BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")

logger.remove()
logger.add(sys.stderr, format="{time:HH:mm:ss} {level} {message}", level="INFO", colorize=False)

# ── Schema ───────────────────────────────────────────────────────────────────
class User(BaseModel):
    id: int
    name: str
    username: str
    email: str

# ── Fetch ────────────────────────────────────────────────────────────────────
async def fetch_users(limit: int = 5) -> list[User]:
    url = f"{BASE_URL}/users"
    logger.info(f"GET {url} (limit={limit})")
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)
        resp.raise_for_status()
    raw = resp.json()[:limit]
    users: list[User] = []
    for item in raw:
        try:
            users.append(User(**item))
        except ValidationError as exc:
            logger.warning(f"skipping malformed record id={item.get('id')}: {exc}")
    logger.info(f"parsed {len(users)} valid users")
    return users

# ── Display ───────────────────────────────────────────────────────────────────
def render_table(users: list[User]) -> None:
    console = Console()
    table = Table(title="Users", show_header=True, header_style="bold cyan")
    table.add_column("ID",       justify="right", style="dim")
    table.add_column("Name",     style="green")
    table.add_column("Username", style="yellow")
    table.add_column("Email")
    for u in users:
        table.add_row(str(u.id), u.name, u.username, u.email)
    console.print(table)

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    users = asyncio.run(fetch_users(limit=5))
    render_table(users)
