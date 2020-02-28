
# imports


import cv2
import time
import datetime
import imutils
import Database
import Test
#db.insertBoi_Boi()
import numpy as np

def motion_detection():
    counter = 0

    video_capture = cv2.VideoCapture(0)  # 0 is default for your default camera
    # May need to be changed for Raspberry Pi
    #NOTE: Raspberry pi is not able to have 2 cameras at the same time. An extra raspberry pi will be required to run the 2nd camera
    #      and detect the motion before sending a "0" or "1" code to the main raspberry pi.
    time.sleep(0.5)

    first_frame = None
    y_coord = Test.array[1]
    y_coord2 = Test.array[3]
    x_coord = Test.array[0]
    x_coord2 = Test.array[2]
    #print(y_coord)


    while True:
        uncropped_frame = video_capture.read()[1]
        text = 'Not Boiling' #Text that shows if no motion is detected. In our case not boiling.
        cv2.imshow("uncropped image", uncropped_frame)
        frame = uncropped_frame[y_coord:y_coord2 ,x_coord:x_coord2]#[100:400,100:500]
        greyscale_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  # Greyscale the frame

        gaussian_frame = cv2.GaussianBlur(greyscale_frame, (21, 21), 0)


        blur_frame = cv2.blur(gaussian_frame, (5, 5))

        greyscale_image = blur_frame

        if first_frame is None:
            first_frame = greyscale_image
        else:
            pass

        frame = imutils.resize(frame, width=500)
        frame_delta = cv2.absdiff(first_frame, greyscale_image)

        thresh = cv2.threshold(frame_delta, 20, 100, cv2.THRESH_BINARY)[1]
        # In the line above, reduce numbers for more sensitivity.
        dilate_image = cv2.dilate(thresh, None, iterations=2)

        cnt = cv2.findContours(dilate_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnt[-2]:
            #time.sleep(0.01)
            if cv2.contourArea(c) > 400:  # if contour area is less then 800 non-zero(not-black) pixels(white)
                (x, y, w, h) = cv2.boundingRect(c)  # x,y are the top left of the contour and w,h are the width and height

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0),2)  # (0, 255, 0) = color R,G,B = lime / 2 = thickness

                #text = 'Boiling'
                counter = counter + 2.5
                # text that appears when there is motion in video feed
                if counter >64:
                    text = 'Boiling'
                    if counter > 72:
                        counter =68
                        pass
                pass

            if cv2.contourArea(c)<400:
                counter = counter - 0.1
                if counter <= 0:
                    counter = 0

                #text = 'Not Boiling'
                pass
            else:
                pass
        counter = counter - 2
        if counter <=0:
            counter = 0

        #TimeStamps
        font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.putText(frame, '{+} Water Status: %s' % (text), (10, 20), cv2.FONT_ITALIC, 0.5, (0, 0, 255), 2)

        cv2.putText(frame, datetime.datetime.now().strftime('%A %d %B %Y %I:%M:%S%p'),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255),1)

        cv2.imshow('Image', frame)
        cv2.imshow('Threshold(foreground mask)', dilate_image)
        cv2.imshow('Frame_delta', frame_delta)
        if counter >= 64:
            print("TRUE")

            #text = "boiling"
            first_frame = greyscale_image
            print("counter", counter)
            Database.dbsend("1")
            time.sleep(0.25) # polling rate
            #Create output variable
            #print(cnt)




        else:
            print("FALSE")

            first_frame = greyscale_image
            print("counter ", counter)
            Database.dbsend("0")
            time.sleep(0.25) #polling rate
            #Create Output Variable
            #print(cnt)





        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    motion_detection()
