import cv2
import numpy as np
import imutils
import time

cropping = 0

x_start, y_start, x_end, y_end = 0, 0, 0, 0

cap = cv2.VideoCapture(0)
ret, image = cap.read()
oriImage = image.copy()


def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping

    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping == 1

    # Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == 1:
            x_end, y_end = x, y

    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = 0 # cropping is finished


        refPoint = [(x_start, y_start), (x_end, y_end)]

        if len(refPoint) == 2: #when two points were found
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            cv2.imshow("Cropped", roi)







cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_crop)

while True:

    i = image.copy()

    if cropping == 0:
        if x_start == x_end:
            cv2.imshow("image", image)
        else:
            cap.release()
            break



    elif cropping ==1:
        cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
        cv2.imshow("image", i)




    cv2.waitKey(1)
print(x_start,y_start,x_end,y_end)
array = [x_start,y_start,x_end,y_end]
print(array)
# close all open windows
cv2.destroyAllWindows()
