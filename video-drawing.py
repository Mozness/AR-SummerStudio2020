from imutils.video import VideoStream
import cv2
import imutils
import boxdrawing
import colourdetection
import dbfunction as db

#press = 'press'
#p_data = 'p_data'

# grab the reference to the webcam. src = 0: laptop webcam. src = 1: usb webcam
vs = VideoStream(src=1).start()

# keep looping
while True:
    # grab the current frame
    frame = vs.read()

    # if we are viewing a video and we did not grab a frame, then we have reached the end of the video
    if frame is None:
        break

    # resize the frame
    frame = imutils.resize(frame, width=1200)

    # box 1 – red
    center1 = colourdetection.colour_center(frame, "red")
    boxdrawing.draw_box(frame, center1, ("left","top"), ("Pressure", db.getPressure()))

    # box 2 – green
    center2 = colourdetection.colour_center(frame, "green")
    boxdrawing.draw_box(frame, center2, ("right","top"), ("Temperature", db.getTemp()))

    # box 3 – blue
    center3 = colourdetection.colour_center(frame, "blue")
    boxdrawing.draw_box(frame, center3, ("left","bottom"), ("Humidity", db.getHum()))

    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# stop the camera video stream and close all windows
vs.stop()
cv2.destroyAllWindows()