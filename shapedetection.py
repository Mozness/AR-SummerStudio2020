import cv2
import imutils
import numpy as np



def ShapeDetector(src, colour_hsv):
    font = cv2.FONT_HERSHEY_COMPLEX

    blurred = cv2.GaussianBlur(src, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, colour_hsv[0], colour_hsv[1])
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Contours detection
    if int(cv2.__version__[0]) > 3:
        # Opencv 4.x.x
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        # Opencv 3.x.x
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        # x = approx.ravel()[0]
        # y = approx.ravel()[1]

        if area > 400:
            # cv2.drawContours(src, [approx], 0, (0, 0, 0), 5)
            if len(approx) == 4:
                (x, y, w, h) = cv2.boundingRect(approx)
                x, y = x+int(w/2), y+int(h/2)
                # cv2.putText(src, "Rectangle", (x, y), font, 1, (0, 0, 0))
                return (x, y)

            # other shapes detection
            # elif len(approx) == 3:
            #     cv2.putText(frame, "Triangle", (x, y), font, 1, (0, 0, 0))
            # elif len(approx) == 4:
            #     (x, y, w, h) = cv2.boundingRect(approx)
            #     ar = w / float(h)
            #     if ar >= 0.95 and ar <= 1.05:
            #         cv2.putText(frame, "Square", (x, y), font, 1, (0, 0, 0))
            #     else:
            #         cv2.putText(frame, "Rectangle", (x, y), font, 1, (0, 0, 0))
            # elif len(approx) == 5:
            #     cv2.putText(frame, "Pentagon", (x, y), font, 1, (0, 0, 0))
            # elif 5 < len(approx) < 15:
            #     cv2.putText(src, "Circle", (x, y), font, 1, (0, 0, 0))