import cv2
import numpy as np
from ultralytics import YOLO

from CameraView import CameraView
from coordinate_determination import ViewCoordinateDetermination
from object_clustering import ObjectClustering


class VideoDetection:

    def __init__(self, video_views: list[CameraView], model_name: str = 'yolo11n.pt'):
        self.video_views = video_views
        self.model = YOLO(model_name)
        self.clustering_processor = ObjectClustering(eps=0.7)
        self.coordinate_processors = {
            i: ViewCoordinateDetermination(
                scale=view.scale,
                center=view.center,
                K=view.K,
                R=view.R,
                T=view.T,
            ) for i, view in enumerate(self.video_views)
        }

    def draw_people(self, clusters, frames):
        for cluster in clusters:
            for camera in clusters[cluster]['cameras']:
                x1, y1, x2, y2 = clusters[cluster]['cameras'][camera]
                X, Y = clusters[cluster]['mean']
                if len(clusters[cluster]['points']) > 1:
                    color = (0, 255, 255)
                else:
                    color = (0, 255, 0)
                frame = frames[camera]
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"Person X={round(X, 2)}, Y={round(Y, 2)}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        for index, frame in enumerate(frames):
            cv2.imshow(f"Video {index}", frame)

    def process_boxes(self, boxex, index: int):
        result = []
        for box in boxex:
            if int(box.cls[0]) == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # координаты бокса
                # нижняя точка бокса (центр низа)
                u = float((x1 + x2) / 2)
                v = float(y2)
                coordinate_processor = self.coordinate_processors[index]
                x, y = coordinate_processor.get_coordinates_by_pixel(u, v)
                result.append([index, [x1, y1, x2, y2], [x, y]])
        return result

    def run(self):
        captures = [cv2.VideoCapture(view.video_stream) for view in self.video_views]
        while True:
            frames = []
            return_status = []
            for capture in captures:
                ret, frame = capture.read()
                frames.append(frame)
                return_status.append(ret)
            if any([not(ret) for ret in return_status]):
                break
            peoples = [self.process_boxes(self.model(frame)[0].boxes, index) for index, frame in enumerate(frames)]
            peoples = [i for j in peoples for i in j]
            cameras = [item[0] for item in peoples]
            pixels = [item[1] for item in peoples]
            points = np.array([item[2] for item in peoples])  # Nx2 или Nx3 массив координат людей
            clusters = self.clustering_processor.get_clusters(cameras, pixels, points)
            self.draw_people(clusters, frames)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
