from rich import print as rprint
from rich.table import Table
from rich.console import Console

# rich.print auto-highlights dicts, lists, and exceptions
rprint({"library": "rich", "version": "15.0.0", "stars": 50000})
# => {'library': 'rich', 'version': '15.0.0', 'stars': 50000}

# A table takes five lines instead of hand-crafting ASCII borders
console = Console()
table = Table(title="Top Libraries", show_header=True, header_style="bold")
table.add_column("Library", style="cyan")
table.add_column("Purpose")
table.add_column("Version", justify="right")

table.add_row("requests",  "HTTP client (sync)",        "2.34.2")
table.add_row("httpx",     "HTTP client (sync + async)", "0.28.1")
table.add_row("pydantic",  "Data validation",           "2.13.4")

console.print(table)
# (renders a formatted table with borders and colors in any terminal)

# One line for pretty tracebacks everywhere:
# from rich.traceback import install; install(show_locals=True)
