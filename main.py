import settings
from video_detection import VideoDetection


if __name__ == '__main__':
    if len(settings.VIEWS) == 0:
        print('Need at list one video stream or video file for running')
    v = VideoDetection(settings.VIEWS, settings.OUT_SIZE, settings.RANGE_X, settings.RANGE_Y, settings.STREAM,
                       settings.OUT_NAME, model_name=settings.MODEL, object_class=settings.OBJECT_CLASS)
    v.run()
