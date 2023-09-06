import cv2
import threading
from PIL import Image, ImageTk

class MediaPlayer:
    cap = None
    video_thread = None
    video_playing = False
    video_paused = False
    video_frame = None
    def __init__(self):
        pass