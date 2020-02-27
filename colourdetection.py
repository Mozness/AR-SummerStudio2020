import cv2
import imutils
import numpy as np

# how to find hsv. put rgb inside the brackets and it will print hsv.
# make the range about (+-10,+-50,+-50). if colour is not detected try (-10, 100, 100) – (+10, 255, 255)
colour = np.uint8([[[40, 50, 155]]])
hsv_colour = cv2.cvtColor(colour, cv2.COLOR_BGR2HSV)
print(hsv_colour)


def colour_center(src, colour):
    # define the lower and upper boundaries of the HSV color space
    if colour == "green":
        # colour_hsv = ((29, 86, 6), (64, 255, 255)) # light green, but not too light
        colour_hsv = ((80, 200, 50), (100, 255, 150))  # more darker green

    if colour == "blue":
        colour_hsv = ((110, 100, 100), (130, 255, 255))  # dark blue

    if colour == "red":
        colour_hsv = ((5, 124, 99), (160, 65, 51))  # original red> ((0, 140, 100), (20, 200, 200))  # bright red (40,50,155) [[[  3 189 155]]]
        # colour_hsv = ((165, 50, 50), (195, 255, 255)) # burgundy red
        # colour_hsv = ((165, 100, 40), (185, 200, 140)) # another burgundy red
    # brown = ((0, 140, 100), (30, 200, 160))
    # yellow = ((20, 100, 100), (30, 255, 255)) # kinda typical yellow

    lower_colour = colour_hsv[0]
    upper_colour = colour_hsv[1]

    # blur the frame, and convert it to the HSV color space
    blurred = cv2.GaussianBlur(src, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color, perform a series of dilations and erosions to remove any small blobs left in  mask
    mask = cv2.inRange(hsv, lower_colour, upper_colour)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current (x, y) center of the colour
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    return center
