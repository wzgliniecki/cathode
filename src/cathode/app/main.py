from textual.app import App, ComposeResult
from textual.widgets import Static
from textual import events

import time

from cathode.app.layout import MainLayout
from cathode.app.input import CameraInput
from cathode.config.settings import RenderSettings, DevSettings


class CathodeApp(App):
    CSS_PATH = "../styles/cathode.css"
    THEMES = ["retro", "amber", "blue", "matrix"]

    def next_theme(self):
        for theme in self.THEMES:
            self.screen.remove_class(theme)

        self.current_theme_index = (self.current_theme_index + 1) % len(self.THEMES)
        new_theme = self.THEMES[self.current_theme_index]

        self.screen.add_class(new_theme)

    def __init__(
        self,
        max_fps: int = RenderSettings.max_fps,
        image_width: int = RenderSettings.image_width,
        image_height: int = RenderSettings.image_height,
        max_frames: int | None = DevSettings.max_frames,
    ):
        super().__init__()

        RenderSettings.max_fps = max_fps
        RenderSettings.image_width = image_width
        RenderSettings.image_height = image_height

        DevSettings.max_frames = max_frames

        self.log("Render settings")
        self.log(f"FPS: {RenderSettings.max_fps}")

        self.cam = CameraInput(
            target_size=(RenderSettings.image_width, RenderSettings.image_height)
        )

        self.main_layout = MainLayout()

        # FPS
        self.current_frame_time = 0.0

        # For Debug and testing - frame counter for earlier exit
        self.frames = 0

        self.current_converter_name = "ascii"
        self.current_effect_names = []

        self.current_theme_index = 0

    def next_converter(self) -> None:
        if self.current_converter_name == "ascii":
            self.current_converter_name = "color_blocks"
        else:
            self.current_converter_name = "ascii"

    def compose(self) -> ComposeResult:
        yield Static(self.main_layout.layout)

    async def on_mount(self):
        self.set_interval(1 / RenderSettings.max_fps, self.update_frame)

    def update_frame(self):
        start = time.perf_counter()

        frame = self.cam.read()

        self.main_layout.update(
            current_frame_time=self.current_frame_time,
            frame=frame,
            user_input=None,  # separate async method
            current_converter_name=self.current_converter_name,
        )

        self.query_one(Static).update(self.main_layout.layout)

        # FPS
        end = time.perf_counter()
        self.current_frame_time = end - start

        # Max frames (dev mode)
        if DevSettings.max_frames is not None:
            self.frames += 1
            if self.frames > DevSettings.max_frames:
                self.exit()

    async def on_key(self, event: events.Key):
        key = event.key

        # move to next style
        if key == "space":
            self.next_theme()
            self.screen.refresh()

        # move to the next converter
        elif key == "enter":
            self.next_converter()
            self.main_layout.update(
                current_frame_time=self.current_frame_time,
                frame=None,
                user_input=event.key,
                current_converter_name=self.current_converter_name,
            )
            self.query_one(Static).update(self.main_layout.layout)

        else:
            pass


if __name__ == "__main__":
    CathodeApp().run()
