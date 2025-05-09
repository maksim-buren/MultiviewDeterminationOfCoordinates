# MultiviewDeterminationOfCoordinates  

This project implements object detection in images and determines their spatial coordinates.  

**IMPORTANT!** Object positions are correctly determined only if they lie on a flat surface (Z = 0), as their location is calculated by projecting rays onto the ground plane. This project is **not suitable** for coordinate determination on uneven terrain.  

The YOLO v11 model is used for object detection ([GitHub link](https://github.com/ultralytics/ultralytics)).  

Testing was performed on the **Multiview Object Tracking Dataset** ([Bitbucket link](https://bitbucket.org/merayxu/multiview-object-tracking-dataset/src/master/)).  

## Requirements  
- Python 3 (tested on Python 3.10 and above).  
- Dependencies: Install via `pip install -r requirements.txt`.  
- Recommended: Use a virtual environment.  

## Input Parameters  
To run the program, configure the following parameters:  

1. **Camera data (video streams)**  
   1.1 Path to the video file or stream descriptor  
   1.2 Camera zoom level  
   1.3 Tuple of central pixels (e.g., `(960, 540)` for FullHD)  
   1.4 Camera intrinsic matrix (3×3)  
   1.5 Camera rotation matrix (3×3)  
   1.6 Camera position matrix in space (format: `[[x],[y],[z]]`)  

2. **Output image size** (e.g., `(1920, 1080)`)  
3. **X-coordinate range**  
4. **Y-coordinate range**  
5. **Enable real-time video playback during processing** (disabled by default)  
6. **Output video file path** (MP4 format)  
7. **Path to YOLO model** (can be pre-trained/custom)  
8. **YOLO object class to process** (e.g., `0` for people)  

### Configuration  
These parameters must be set in either:  
- `settings.py`  
- `local_settings.py` (create in the same directory).  

#### Example `local_settings.py`:  
```python
from camera_view import CameraView

VIEWS = (
    CameraView(
        video_stream='view-HC4.mp4',
        scale=1,
        center=(960, 540),
        K=[[2350, 0, 0], [0, 2350, 0], [0, 0, 1]],
        R=[[ 1.        ,  0.        ,  0.        ],
           [ 0.       , -0.08715574, -0.9961947 ],
           [ 0.       ,  0.9961947 , -0.08715574]],
        T=[[0.], [0.], [1.5]]
    ),
    # Add more cameras as needed
)

OUT_SIZE = (1920, 1080)
RANGE_X = (-20, 20)
RANGE_Y = (-5, 35)
STREAM = True
OUT_NAME = 'example.mp4'
```

*The example uses cameras from the test dataset: [Multiview Object Tracking Dataset (Auditorium)](https://bitbucket.org/merayxu/multiview-object-tracking-dataset/src/master/CAMPUS/Auditorium/).*  

### How to Run  
1. Install dependencies and configure settings.  
2. Execute:  
   ```bash  
   python3 main.py  
   ```
## Output Visualization

The system generates a composite video stream with the following structure:

### Camera Feed Display
- **Top section**: Shows synchronized feeds from input cameras  
  *(Note: Only 1-2 camera feeds are displayed visually; all others process data in background)*  
- **Overlay elements**:  
  - 🟡 **Yellow bounding boxes**: Multi-camera detections (≥2 cameras)  
  - 🟢 **Green bounding boxes**: Single-camera detections  

### Coordinate Mapping
- **Bottom section**: Displays 2D ground plane projection with:  
  - 💛 **Yellow markers**: Objects with verified positions (averaged from multiple views)  
  - 💚 **Green markers**: Objects detected by single camera only  

*(Example visualization will be inserted here: [RESULT_VIDEO.mp4])*
