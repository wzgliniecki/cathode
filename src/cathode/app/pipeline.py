import numpy as np

from cathode.converters.base import Converter
from cathode.effects.base import TextEffect, FrameEffect


class Pipeline:
    def __init__(
        self,
        converter: Converter,
        frame_effects: list[FrameEffect],
        text_effects: list[TextEffect],
    ):
        self.converter = converter
        self.frame_effects = frame_effects
        self.text_effects = text_effects

    def update(
        self,
        converter: Converter,
        frame_effects: list[FrameEffect],
        text_effects: list[TextEffect],
    ):
        self.converter = converter
        self.frame_effects = frame_effects
        self.text_effects = text_effects

    def apply(self, frame: np.ndarray) -> str:
        # Frame effects are effectively used for preproccesing
        for fe in self.frame_effects:
            frame = fe.apply(frame)

        text = self.converter.apply(frame)

        # Text effect - after conversion
        for te in self.text_effects:
            text = te.apply(text)

        return text
