import time

from rich.live import Live
from rich.console import Console

from cathode.app.layout import MainLayout
from cathode.app.input import CameraInput
from cathode.config.settings import RenderSettings
from cathode.config.settings import DevSettings


def run() -> None:
    console = Console()
    max_frames = DevSettings.max_frames
    frames = 0
    with Live(console=console, refresh_per_second=RenderSettings.max_fps) as live:
        main_layout = MainLayout()
        current_frame_time = 0.0
        cam = CameraInput(
            target_size=(RenderSettings.image_height, RenderSettings.image_width)
        )

        while True:
            start_time_frame = time.perf_counter()
            frame = cam.read()

            main_layout.update(current_frame_time=current_frame_time, frame=frame)
            live.update(main_layout.layout)

            end_time_frame = time.perf_counter()
            current_frame_time = end_time_frame - start_time_frame
            if max_frames is not None:
                frames += 1
                if frames > max_frames:
                    break
