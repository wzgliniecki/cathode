import cv2
import numpy as np


class CameraInput:
    def __init__(self, index: int = 0, target_size: tuple[int, int] | None = None):
        self.cap = cv2.VideoCapture(index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera at index: {index}")

        self.target_size = target_size

    def read(self) -> np.ndarray | None:
        ok, frame = self.cap.read()
        if not ok:
            return None

        if self.target_size:
            frame = cv2.resize(frame, self.target_size, interpolation=cv2.INTER_AREA)

        return frame

    def release(self):
        self.cap.release()
