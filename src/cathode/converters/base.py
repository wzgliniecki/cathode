from typing import Protocol
import numpy as np


class Converter(Protocol):
    name = ...

    def apply(self, frame: np.ndarray) -> str: ...
