# converters/color_blocks.py
import numpy as np
from .base import Converter


class ColorBlocksConverter(Converter):
    def __init__(self, bits: int):
        self.name = "Color blocks"
        self.bits = bits
        self.cache = self._build_cache(bits)

    def _build_cache(self, bits: int):
        levels = 256 >> bits
        step = 256 // levels

        cache = {}
        for r in range(levels):
            for g in range(levels):
                for b in range(levels):
                    R = r * step
                    G = g * step
                    B = b * step
                    cache[(r, g, b)] = f"[on rgb({R},{G},{B})] [/on rgb({R},{G},{B})]"
        return cache

    def apply(self, frame: np.ndarray) -> str:
        rows = []
        for row in frame:
            line = ""
            for r, g, b in row:
                qr = int(r) >> self.bits
                qg = int(g) >> self.bits
                qb = int(b) >> self.bits
                key = (qr, qg, qb)
                line += self.cache[key]
            rows.append(line)
        return "\n".join(rows)
