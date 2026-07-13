from rich.layout import Layout
from rich.panel import Panel
import psutil


class PerformancePanel:
    """Displays FPS, CPU, and RAM usage in the terminal."""

    def __init__(self, current_time_frame: float) -> None:
        self.current_time_frame = current_time_frame
        self.message = "Initializing..."

    def get_fps_value(self) -> float:
        if self.current_time_frame == 0:
            return 0.0
        temp = 1 / self.current_time_frame
        # TODO - move that to settings and import here
        return 30.0 if temp > 30 else temp

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


class MainLayout:
    def __init__(self) -> None:
        self.layout = Layout()
        self.performance_panel = PerformancePanel(current_time_frame=30.0)

        self.layout.split_row(
            Layout(name="Image", renderable=Panel("Image", title="Image")),
            Layout(name="right"),
        )

        self.layout["right"].split_column(
            Layout(name="Performance"),
            Layout(name="Effects", renderable=Panel("Effects", title="Effects")),
        )

    def update(self, current_frame_time: float) -> None:
        self.performance_panel.update(current_time_frame=current_frame_time)
        self.layout["Performance"].update(self.performance_panel.get_panel())
