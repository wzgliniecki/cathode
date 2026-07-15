from .base import TextEffect


class RainbowEffect(TextEffect):
    name = "Rainbow"

    def apply(self, frame: str) -> str:
        return frame
