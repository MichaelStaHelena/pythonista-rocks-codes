from rich.console import Console
from rich.table import Table

# Console auto-detects TTY; when piped to a file it strips ANSI automatically.
# no_color=True here so the captured output is clean plain text.
console = Console(highlight=False, markup=True, no_color=True)

# Markup renders in-terminal as bold/underline; plain text in pipes/files.
console.print("[bold]Bold text[/bold] and [underline]underline[/underline]")
# => Bold text and underline

table = Table(title="City Weather", show_header=True)
table.add_column("City")
table.add_column("Temp C", justify="right")
table.add_column("Humid %", justify="right")
table.add_row("Berlin", "12.0", "81")
table.add_row("Paris",  "18.1", "63")
console.print(table)
# => (rich renders a bordered table; rows: Berlin 12.0 81 / Paris 18.1 63)
