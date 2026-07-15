import numpy as np
from .base import FrameEffect
from cathode.config.settings import RenderSettings


class ColorCompressionEffect(FrameEffect):
    def __init__(self):
        self.bits = RenderSettings.color_compression_level

    def apply(self, frame: np.ndarray) -> np.ndarray:
        # quantization of colors
        return frame >> self.bits
