import cv2
import numpy as np


class CameraInput:
    def __init__(self, index: int = 0):
        self.cap = cv2.VideoCapture(index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera at index: {index}")

    def read(self) -> np.ndarray | None:
        ok, frame = self.cap.read()
        return frame if ok else None

    def release(self):
        self.cap.release()
