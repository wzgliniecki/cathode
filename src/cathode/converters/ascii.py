from .base import Converter
import numpy as np

ASCII_CHARS = "@%#*+=-:. "


class ASCIIconverter(Converter):
    name = "ascii"

    def apply(self, frame: np.ndarray) -> str:
        # frame is H x W x 3 (RGB)
        # convert to grayscale
        gray = 0.299 * frame[:, :, 0] + 0.587 * frame[:, :, 1] + 0.114 * frame[:, :, 2]

        # normalize to 0..len(ASCII_CHARS)-1
        gray_norm = (gray / 255) * (len(ASCII_CHARS) - 1)
        gray_norm = gray_norm.astype(int)

        rows = []
        for row in gray_norm:
            line = "".join(ASCII_CHARS[val] for val in row)
            rows.append(line)

        return "\n".join(rows)
