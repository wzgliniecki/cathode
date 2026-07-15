from typing import Protocol
import numpy as np


class FrameEffect(Protocol):
    """Frame effect - to be used as a pre-processing method by converters"""

    name = ...

    def apply(self, frame: np.ndarray) -> np.ndarray: ...


class TextEffect(Protocol):
    """Text effect - to be used as a post-processing method after conversion"""

    name = ...

    def apply(self, frame: str) -> str: ...
