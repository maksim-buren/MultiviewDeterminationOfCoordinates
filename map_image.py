import cv2
import numpy as np


class MapImage:

    def __init__(self, width: int, height: int, range_x: tuple[int, int], range_y: tuple[int, int]):
        self.width = width
        self.height = height
        self.range_x = range_x
        self.range_y = range_y
        self.map = self._create_map()
        self.draw_grid()

    def _create_map(self):
        map_img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        map_img.fill(0)
        return map_img

    def draw_grid(self):
        x_min, x_max = self.range_x
        y_min, y_max = self.range_y

        cv2.line(self.map,
                 self.scale_coords(0, y_min),
                 self.scale_coords(0, y_max),
                 (0, 0, 255), 2)
        cv2.line(self.map,
                 self.scale_coords(x_min, 0),
                 self.scale_coords(x_max, 0),
                 (0, 0, 255), 2)

        for x in range(x_min, x_max + 1, 5):
            if x == 0:
                continue
            start = self.scale_coords(x, y_min)
            end = self.scale_coords(x, y_max)
            cv2.line(self.map, start, end, (200, 200, 200), 1)
            cv2.putText(self.map, str(x), (start[0] + 5, self.height - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

        for y in range(y_min, y_max + 1, 5):
            if y == 0:
                continue
            start = self.scale_coords(x_min, y)
            end = self.scale_coords(x_max, y)
            cv2.line(self.map, start, end, (200, 200, 200), 1)
            cv2.putText(self.map, str(y), (10, start[1] - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

    def scale_coords(self, x, y):
        x_norm = (x - self.range_x[0]) / (self.range_x[1] - self.range_x[0])
        y_norm = (y - self.range_y[0]) / (self.range_y[1] - self.range_y[0])

        px = int(x_norm * self.width)
        py = self.height - int(y_norm * self.height)

        return (px, py)

    def draw_objects(self, objects, color=(0, 0, 255)):
        for obj in objects:
            id_, x, y = obj
            px, py = self.scale_coords(x, y)
            cv2.circle(self.map, (px, py), 5, color, -1)
            cv2.putText(self.map, f"id= {id_} ({x:.2f}, {y:.2f})", (px + 10, py),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
