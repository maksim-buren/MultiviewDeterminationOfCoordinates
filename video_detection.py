import cv2
import numpy as np
from ultralytics import YOLO

from camera_view import CameraView
from constants import CAMERA_POINT_COLOR, MULTI_VIEW_COLOR, CAMERA_1_COLOR, CAMERA_2_COLOR, CAMERA_OTHER_COLOR, LEGEND
from coordinate_determination import ViewCoordinateDetermination
from map_image import MapImage
from object_clustering import ObjectClustering


class VideoDetection:

    def __init__(self, video_views: list[CameraView], result_size: tuple[int, int], range_x: tuple[int, int],
                 range_y: tuple[int, int], stream: bool = False, out_name: str = 'result.mp4',
                 model_name: str = 'yolo11n.pt', object_class: int = 0):
        self.stream = stream
        self.object_class = object_class
        self.out_name = out_name
        self.output_width = result_size[0]
        self.output_height = result_size[1]
        self.range_x = range_x
        self.range_y = range_y
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

    def draw_map(self, clusters):
        map_img = MapImage(self.output_width, int(self.output_height/2), self.range_x, self.range_y)
        camera_objects = [(view.video_stream, view.T[0][0], view.T[1][0]) for view in self.video_views]
        map_img.draw_legend(LEGEND)
        map_img.draw_objects(camera_objects, CAMERA_POINT_COLOR)
        peoples_top = [(cluster, *clusters[cluster]['mean']) for cluster in clusters if len(clusters[cluster]['points']) > 1]
        map_img.draw_objects(peoples_top, MULTI_VIEW_COLOR)
        peoples_other_1 = [(cluster, *clusters[cluster]['mean']) for cluster in clusters if
                           len(clusters[cluster]['points']) == 1 and clusters[cluster]['cameras'].get(0) is not None]
        map_img.draw_objects(peoples_other_1, CAMERA_1_COLOR)
        peoples_other_2 = [(cluster, *clusters[cluster]['mean']) for cluster in clusters if
                           len(clusters[cluster]['points']) == 1 and clusters[cluster]['cameras'].get(1) is not None]
        map_img.draw_objects(peoples_other_2, CAMERA_2_COLOR)
        return map_img.map

    def draw_rectangle(self, clusters, frames):
        for cluster in clusters:
            for camera in clusters[cluster]['cameras']:
                x1, y1, x2, y2 = clusters[cluster]['cameras'][camera]
                X, Y = clusters[cluster]['mean']
                if len(clusters[cluster]['points']) > 1:
                    color = MULTI_VIEW_COLOR
                else:
                    if clusters[cluster]['cameras'].get(0) is not None:
                        color = CAMERA_1_COLOR
                    elif clusters[cluster]['cameras'].get(1) is not None:
                        color = CAMERA_2_COLOR
                    else:
                        color = CAMERA_OTHER_COLOR
                frame = frames[camera]
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"Id = {cluster} {X:.2f}, {Y:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def draw_people(self, clusters, frames, out):
        self.draw_rectangle(clusters, frames)
        if len(frames) > 1:
            frame1 = cv2.resize(frames[0], (self.output_width//2, self.output_height//2))
            frame2 = cv2.resize(frames[1], (self.output_width//2, self.output_height//2))
            combined_frame = np.hstack((frame1, frame2))
        else:
            combined_frame = cv2.resize(frames[0], (self.output_width, self.output_height//2))
        map_img = self.draw_map(clusters)
        final_output = np.vstack((combined_frame, map_img))
        if self.stream:
            cv2.imshow("Combined Videos", final_output)
        out.write(final_output)

    def process_boxes(self, boxex, index: int):
        result = []
        for box in boxex:
            if int(box.cls[0]) == self.object_class:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                u = float((x1 + x2) / 2)
                v = float(y2)
                coordinate_processor = self.coordinate_processors[index]
                x, y = coordinate_processor.get_coordinates_by_pixel(u, v)
                result.append([index, [x1, y1, x2, y2], [x, y]])
        return result

    def run(self):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.out_name, fourcc, 30, (self.output_width, self.output_height))
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
            points = np.array([item[2] for item in peoples])
            clusters = self.clustering_processor.get_clusters(cameras, pixels, points)
            self.draw_people(clusters, frames, out)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        for capture in captures:
            capture.release()
        out.release()
        cv2.destroyAllWindows()
