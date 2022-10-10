from dataclasses import replace
import math
import socket
import struct
import gbvision as gbv
import cv2 
import numpy as np
import settings as settings
from track_object import track_object

cam = gbv.USBCamera(settings.CAMERA_PORT, gbv.CameraData(777.3291449774972,1.0402162342 , 0.86742863824, name="limelight"))
blue_obj = track_object(cam=cam, pid_vals=[110, 253, 154], hue=[settings.HUE_KP, settings.HUE_KI,
                        settings.HUE_KD], sat=[settings.SAT_KP, settings.SAT_KI,
                        settings.SAT_KD], val=[settings.VAL_KP, settings.VAL_KI, settings.VAL_KD],
                        range=[5, 40, 60], target= gbv.GameObject(0.212694462109))
red_obj = track_object(cam=cam, pid_vals=[0, 255, 142], hue=[settings.HUE_KP, settings.HUE_KI,
                        settings.HUE_KD], sat=[settings.SAT_KP, settings.SAT_KI,
                        settings.SAT_KD], val=[settings.VAL_KP, settings.VAL_KI, settings.VAL_KD],
                        range=[5, 40, 60], target=gbv.GameObject(0.212694462109))
hub_obj = track_object(cam=cam, pid_vals=[94, 118, 202], hue=[settings.HUE_KP, settings.HUE_KI,
                        settings.HUE_KD], sat=[settings.SAT_KP, settings.SAT_KI,
                        settings.SAT_KD], val=[settings.VAL_KP, settings.VAL_KI, settings.VAL_KD],
                        range=[10, 110, 90], target= gbv.GameObject(0.13490737563232041))
balls_port = 5801
hub_port = 5800
balls_mode = 0
hub_mode = 1
def runPipeline(image, llrobot):
    global blue_obj
    global red_obj 
    global hub_obj
    global balls_port
    global hub_port
    global cam
    global balls_mode
    global hub_mode
    
    cam.width = 960
    cam.height = 720
    # balls
    obj = blue_obj # switch between blue and red
    
    port = balls_port
    obj.cam = cam
    obj.track_cycle(image, mode)

    mode = balls_mode
    frame = image
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
    
    
    # hub:
    mode = hub_mode
    port = hub_port
    obj = hub_obj
    obj.cam = cam
    obj.track_cycle(image, mode)
    
    largestContour = ()
    frame = gbv.draw_rotated_rects(
        image, obj.get_rects(), (255, 0, 0), thickness=5)
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