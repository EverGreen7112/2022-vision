import math
import socket
import struct
import gbvision as gbv
import cv2 
import numpy as np
import settings as settings
from track_object import track_object

denoise_hub = gbv.MedianBlur(3) + gbv.Dilate(5, 2) + gbv.Erode(5, 2) + gbv.DistanceTransformThreshold(0.1)
denoise_red = gbv.MedianBlur(3) + gbv.Dilate(5, 2) + gbv.Erode(5, 2) + gbv.DistanceTransformThreshold(0.1)
denoise_blue = gbv.MedianBlur(3) + gbv.Dilate(5, 2) + gbv.Erode(5, 2) + gbv.DistanceTransformThreshold(0.1)
cam = gbv.USBCamera(settings.CAMERA_PORT, gbv.CameraData(777.3291449774972,1.0402162342 , 0.86742863824, pitch_angle=math.radians(35.5), name="limelight"))
blue_obj = track_object(cam=cam, pid_vals=[110, 253, 154],
                        hue=[settings.HUE_KP, settings.HUE_KI, settings.HUE_KD], sat=[settings.SAT_KP, settings.SAT_KI, settings.SAT_KD], val=[settings.VAL_KP, settings.VAL_KI, settings.VAL_KD],
                        range=[5, 40, 60], target= gbv.GameObject(0.212694462109), denoise_pipe = denoise_blue)
red_obj = track_object(cam=cam, pid_vals=[0, 255, 142], 
                        hue=[settings.HUE_KP, settings.HUE_KI,settings.HUE_KD], sat=[settings.SAT_KP, settings.SAT_KI,settings.SAT_KD], val=[settings.VAL_KP, settings.VAL_KI, settings.VAL_KD],
                        range=[5, 40, 60], target=gbv.GameObject(0.212694462109), denoise_pipe = denoise_red)
hub_obj = track_object(cam=cam, pid_vals=[94, 213, 216],
                        hue=[settings.HUE_KP, settings.HUE_KI, settings.HUE_KD], sat=[settings.SAT_KP, settings.SAT_KI, settings.SAT_KD], val=[settings.VAL_KP, settings.VAL_KI, settings.VAL_KD],
                        range=[10, 110, 90], target= gbv.GameObject(0.13490737563232041), denoise_pipe = denoise_hub)

def runPipeline(image, llrobot):
    global blue_obj
    global red_obj 
    global hub_obj
    global cam
    mode = settings.HUB_MODE
    cam.width = 960
    cam.height = 720
    
    
    port = settings.HUB_PORT
    obj = hub_obj
    obj.cam = cam
    obj.track_cycle(image, mode)

    frame = image
    largestContour = ()
    if mode == settings.HUB_MODE:
        frame = gbv.draw_rotated_rects(
            image, obj.get_rects(), (255, 0, 0), thickness=5)
    elif mode == settings.BALLS_MODE:
        frame = gbv.draw_circles(
            image, obj.get_circs(), (255, 0, 0), thickness=5)
    try:
        frame2 = gbv.draw_rotated_rects(frame, [obj.get_bbox()], (0, 0, 255), thickness=5)
        frame = frame2
    except:
        pass

    locals = obj.get_locals()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(struct.pack('fff', locals[0], locals[1], locals[2]),
                    ("255.255.255.255", port))
    
    
    return largestContour, frame, locals