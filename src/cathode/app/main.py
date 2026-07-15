from rich.live import Live
from rich.console import Console
from cathode.app.layout import MainLayout
from cathode.app.input import CameraInput
import time


def run() -> None:
    console = Console()
    max_frames = 300
    frames = 0
    with Live(console=console, refresh_per_second=30) as live:
        main_layout = MainLayout()
        current_frame_time = 0.0
        cam = CameraInput()

        while True:
            start_time_frame = time.perf_counter()
            frame = cam.read()

            main_layout.update(current_frame_time=current_frame_time, frame=frame)
            live.update(main_layout.layout)

            end_time_frame = time.perf_counter()
            current_frame_time = end_time_frame - start_time_frame
            frames += 1
            if frames > max_frames:
                break
