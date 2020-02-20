from imutils.video import VideoStream
import cv2
import imutils
import boxdrawing
from shapedetection.shapedetection import ShapeDetector

# grab the reference to the webcam
cap = cv2.VideoCapture(0)

# keep looping
while True:
    # grab the current frame
    _, frame = cap.read()

    # if we are viewing a video and we did not grab a frame, then we have reached the end of the video
    if frame is None:
        break

    # resize the frame
    frame = imutils.resize(frame, width=1200)

    # highilighers colours
    blue_hsv = ((90, 100, 140), (120, 200, 255))     # blue      (190, 130, 75)      [[[106 154 190]]]
    purple_hsv = ((128, 30, 100), (148, 120, 200))   # purple    (150, 100, 130)     [[[138  85 150]]]
    pink_hsv = ((158, 50, 150), (178, 200, 255))     # pink      (145, 100, 215)     [[[168 136 215]]]

    # box 1 – blue
    center1 = ShapeDetector(frame, blue_hsv)
    boxdrawing.draw_box(frame, center1, ("left","top"), ("Pressure", "0 kPa"))

    # box 2 – purple
    center2 = ShapeDetector(frame, purple_hsv)
    boxdrawing.draw_box(frame, center2, ("right","top"), ("Temperature", "23 deg"))

    # box 3 – pink
    center3 = ShapeDetector(frame, pink_hsv)
    boxdrawing.draw_box(frame, center3, ("left","bottom"), ("Humidity", "million"))

    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# stop the camera video stream and close all windows
cap.release()
cv2.destroyAllWindows()
