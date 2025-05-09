from camera_view import CameraView

# List with camera params
VIEWS = ()
# Out video size
OUT_SIZE = (1920, 1080)
# Range cordinates
RANGE_X = (-50, 50)
RANGE_Y = (-50, 50)
# Run out video while processing
STREAM = False
# Out video file name
OUT_NAME = 'result.mp4'
# YOLO model name
MODEL = 'yolo11n.pt'
# YOLO object class for detection and coordinates determination (0 - people)
OBJECT_CLASS = 0

try:
    from local_settings import *
except ImportError:
    pass
