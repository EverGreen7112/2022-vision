import cv2
import numpy as np
import gbvision as gbv
stdv = np.array([5, 40, 60])
# stdv = np.array([0, 0, 0])

# basically this whole piece of code is here to write the HSV values to thr.txt


def main():
    # camera = gbv.USBCamera(settings.CAMERA_PORT, gbv.CameraData(23.65066003307307,1.0402162342 , 0.86742863824, name="limelight"))
    # camera.set_exposure(settings.EXPOSURE)
    # window = gbv.CameraWindow('feed', camera)
    window = gbv.FeedWindow("feed")
    window.open()
    img = cv2.imread('thr.jpg')
    while True:
        # frame = window.show_and_get_frame()
        # ok, frame = camera.read()
        window.show_frame(img)
        frame = img

        k = window.last_key_pressed
        if k == 'r':
            bbox = cv2.selectROI('feed', frame)
            
            thr = gbv.median_threshold(frame, stdv, bbox, 'HSV')
        
            print(thr)
            print(gbv.median_threshold(frame, [0, 0, 0], bbox, 'HSV'))
            break
    cv2.destroyAllWindows()

    original = gbv.FeedWindow(window_name='original')
    after_proc = gbv.FeedWindow(window_name='after threshold', drawing_pipeline=thr)

    original.open()
    after_proc.open()
    while True:
        # ok, frame = camera.read()
        frame = img
        if not original.show_frame(frame):
            break
        if not after_proc.show_frame(frame):
            break

    exit()


if __name__ == '__main__':
    main()