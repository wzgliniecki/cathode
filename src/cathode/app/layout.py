from rich.layout import Layout
from rich.panel import Panel
import psutil
import numpy as np
from cathode.config.settings import RenderSettings
from .pipeline import Pipeline
from cathode.converters.base import Converter
from cathode.converters.color_blocks import ColorBlocksConverter
from cathode.converters.ascii import ASCIIconverter
from cathode.layouts.effects_layout import EffectsLayout


class PerformancePanel:
    """Displays FPS, CPU, and RAM usage in the terminal."""

    def __init__(self, current_time_frame: float) -> None:
        self.current_time_frame = current_time_frame
        self.message = "Initializing..."

    def get_fps_value(self) -> float:
        if self.current_time_frame == 0:
            return 0.0
        temp = 1 / self.current_time_frame
        return float(RenderSettings.max_fps) if temp > RenderSettings.max_fps else temp

    def update(self, current_time_frame: float) -> None:
        # FPS
        self.current_time_frame = current_time_frame

        # CPU
        cpu_percent = psutil.cpu_percent(interval=None)
        cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)
        cpu_count_logical = psutil.cpu_count()

        # RAM
        mem = psutil.virtual_memory()
        ram_total = mem.total
        ram_used = mem.used
        ram_percent = mem.percent

        self.message = (
            f"FPS: {self.get_fps_value():.2f}\n"
            f"CPU: {cpu_percent:.1f}% ({cpu_count_logical} threads)\n"
            f"CPU per core: {cpu_per_core}\n"
            f"RAM: {ram_percent:.1f}% ({ram_used / 1e9:.2f} / {ram_total / 1e9:.2f} GB)\n"
        )

    def get_panel(self) -> Panel:
        return Panel(self.message, title="Performance")


class ImagePanel:
    def __init__(self, frame: np.ndarray | None) -> None:
        self.frame = frame
        self.bits = RenderSettings.color_compression_level
        self.converter_classes = {
            "color_blocks": ColorBlocksConverter,
            "ascii": ASCIIconverter,
        }
        # self.current_converter = self.converter_classes["color_blocks"](bits=RenderSettings.color_compression_level)
        self.current_converter = self.converter_classes["ascii"]()

        self.pipeline = Pipeline(
            converter=self.current_converter,
            frame_effects=[],
            text_effects=[],
        )

    def update(self, frame: np.ndarray | None) -> None:
        if frame is not None:
            self.frame = frame

    def get_panel(self) -> Panel:
        if self.frame is None:
            text = "No input data"
        else:
            text = self.pipeline.apply(self.frame)
        return Panel(text, title="Image")


class MainLayout:
    def __init__(self) -> None:
        self.layout = Layout()
        self.performance_panel = PerformancePanel(
            current_time_frame=RenderSettings.max_fps
        )
        self.image_panel = ImagePanel(frame=None)
        self.effects_layout = EffectsLayout(current_converter="ascii")

        self.layout.split_row(
            Layout(name="Image"),
            Layout(name="right"),
        )

        self.layout["right"].split_column(
            Layout(name="Performance"),
            Layout(name="Effects"),
        )

    def update(self, current_frame_time: float, frame: np.ndarray | None, 
               user_input: str | None) -> None:
        self.performance_panel.update(current_time_frame=current_frame_time)
        self.layout["Performance"].update(self.performance_panel.get_panel())
        self.image_panel.update(frame=frame)
        self.layout["Image"].update(self.image_panel.get_panel())
        if user_input is not None:
            self.effects_layout.update(user_input)
        self.layout["Effects"].update(self.effects_layout.get_panel())
