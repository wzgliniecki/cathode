from dataclasses import dataclass


@dataclass
class RenderSettings:
    """General settings"""

    image_width: int = 40
    image_height: int = 20
    max_fps: int = 30
    color_compression_level: int = 3

    def validate(self):
        if self.image_width <= 0:
            raise ValueError("image_width must be positive")
        if self.image_height <= 0:
            raise ValueError("image_height must be positive")
        if self.max_fps <= 0:
            raise ValueError("max_fps must be positive")
        if not (0 <= self.color_compression_level <= 7):
            raise ValueError("color_compression_level must be between 0 and 7")


@dataclass
class DevSettings:
    """Settings relevant for debugging and development"""

    max_frames: int | None = None

    def validate(self):
        if self.max_frames is not None and self.max_frames <= 0:
            raise ValueError("image_width must be positive")
