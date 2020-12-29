import time
import os
import sys
try:
    import numpy as np
    import cv2
    import cvlib as cv
    import matplotlib.pyplot as plt
    from cvlib.object_detection import draw_bbox
except Exception as e:
    print(e)
    os.system('pip install cv2 & pip install cvlib & pip install matplotlib.pyplot & pip install numpy')
    os.system('humandetec.py')
print("Пуск скрипта")

def PersonD():
    cv2.startWindowThread()

    cap = cv2.VideoCapture(1)

    cap1.set(cv2.CAP_PROP_FPS, int(15))

    # the output will be written to output.avi
    out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'MJPG'),15., (640,480))
    print("Пуск камеры")
    while(True):
        # Capture frame-by-frame
        ret, frame = cap1.read()

        # resizing for faster detection
        frame = cv2.resize(frame, (640, 480))
        # detect people in the image
        # returns the bounding boxes for the detected objects
        bbox, label, conf = cv.detect_common_objects(frame)
        output_image = draw_bbox(frame, bbox, label, conf)
        
        # Write the output video 
        if 'person' in label:
            print("Тело найдено!!" + str(conf))
            cv2.imwrite("PersonHere.jpg", frame)
            out.write(frame.astype('uint8'))
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap1.release()
    # and release the output
    out.release()
    # finally, close the window
    cv2.destroyAllWindows()
    cv2.waitKey(1)
