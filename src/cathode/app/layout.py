from rich.layout import Layout
from rich.panel import Panel
import psutil
import numpy as np
from PIL import Image


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


class ImagePanel:
    def __init__(self, frame: np.ndarray | None) -> None:
        self.frame = frame
        self.bits = 3

        def build_cache():
            levels = 256 >> self.bits  # number of quantization levels
            step = 256 // levels  # spacing between colors

            cache = {}
            for r in range(levels):
                for g in range(levels):
                    for b in range(levels):
                        R = r * step
                        G = g * step
                        B = b * step
                        cache[(r, g, b)] = (
                            f"[on rgb({R},{G},{B})] [/on rgb({R},{G},{B})]"
                        )
            return cache

        self.BLOCK_CACHE = build_cache()

    def get_transformed_image(self) -> str:
        if self.frame is None:
            return "No input data"

        def quantize_rgb(r, g, b, bits=self.bits):
            return (r >> bits, g >> bits, b >> bits)

        # Hardcoded resolution
        # TODO - change it
        target_w = 50
        target_h = 25

        # Convert BGR → RGB
        rgb = self.frame[:, :, ::-1].astype("uint8")

        # Resize using Pillow
        img = Image.fromarray(rgb)
        img = img.resize((target_w, target_h), Image.Resampling.BILINEAR)

        small = np.array(img)  # shape (H, W, 3)

        rows = []
        for row in small:
            line = ""
            for r, g, b in row:
                # Rich color tag
                r, g, b = quantize_rgb(r, g, b)
                key = (int(r), int(g), int(b))
                line += self.BLOCK_CACHE[key]
            rows.append(line)

        return "\n".join(rows)

    def update(self, frame: np.ndarray | None) -> None:
        if frame is not None:
            self.frame = frame

    def get_panel(self) -> Panel:
        return Panel(self.get_transformed_image(), title="Image")


class MainLayout:
    def __init__(self) -> None:
        self.layout = Layout()
        self.performance_panel = PerformancePanel(current_time_frame=30.0)
        self.image_panel = ImagePanel(frame=None)

        self.layout.split_row(
            Layout(name="Image"),
            Layout(name="right"),
        )

        self.layout["right"].split_column(
            Layout(name="Performance"),
            Layout(name="Effects", renderable=Panel("Effects", title="Effects")),
        )

    def update(self, current_frame_time: float, frame: np.ndarray | None) -> None:
        self.performance_panel.update(current_time_frame=current_frame_time)
        self.layout["Performance"].update(self.performance_panel.get_panel())
        self.image_panel.update(frame=frame)
        self.layout["Image"].update(self.image_panel.get_panel())
