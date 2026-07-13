from rich.live import Live
from rich.console import Console


def run() -> None:
    console = Console()

    initial_message = "Cathode starting..."

    with Live(initial_message, console=console, refresh_per_second=30) as live:
        while True:
            # TODO - whole project

            live.update(initial_message)
