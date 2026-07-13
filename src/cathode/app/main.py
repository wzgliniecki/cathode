from rich.live import Live
from rich.console import Console
from cathode.app.layout import MainLayout
import time


def run() -> None:
    console = Console()

    with Live(console=console, refresh_per_second=30) as live:
        main_layout = MainLayout()
        current_frame_time = 0.0

        while True:
            start_time_frame = time.perf_counter()

            main_layout.update(current_frame_time=current_frame_time)
            live.update(main_layout.layout)

            end_time_frame = time.perf_counter()
            current_frame_time = end_time_frame - start_time_frame
