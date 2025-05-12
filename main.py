import sys

import settings
from rotating_matrix import RotationMatrix
from video_detection import VideoDetection


if __name__ == '__main__':
    command = 'run'
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'rotating_matrix':
            n = len(sys.argv)
            if n == 5:
                x, y, z = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
                print(RotationMatrix.euler_rotation_matrix(z, y, x))
            else:
                print('Please input angles x, y and z in degrees after commands')
        elif command == 'run':
            pass
    if command == 'run':
        if len(settings.VIEWS) == 0:
            print('Need at list one video stream or video file for running')
        v = VideoDetection(settings.VIEWS, settings.OUT_SIZE, settings.RANGE_X, settings.RANGE_Y, settings.STREAM,
                           settings.OUT_NAME, model_name=settings.MODEL, object_class=settings.OBJECT_CLASS)
        v.run()
