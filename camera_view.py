import numpy as np


class CameraView:

    def __init__(self, video_stream: str, scale: float, center: tuple[int, int], K: list[list[int]],
                 R: list[list[float]], T: list[list[float]]):
        self.video_stream = video_stream
        self.scale = scale
        self.center = center
        self.K = np.array(K)
        self.R = np.array(R)
        self.T = np.array(T)
