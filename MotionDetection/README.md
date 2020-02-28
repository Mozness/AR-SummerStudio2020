# MOTION DETECTION FOR AUGMENTED REALITY (2020)
</br>
Motion sensing code must be run separately from main code. </br>
This AR program was built in Pycharm. Run the video-drawing class to run the program. </br>
There are two main Files </br>
- MotionDetectionWithoutDatabase.py runs the motion detection without the use of a database </br>
- MotionDetectionWithDatabase.py requires the database to be running </br>
NOTE: The database listed above is not the same as Database.py . Database.py is used to allow the sending of data to the actual Database </br>
The "Crop.py" file is used by both main files and is used to crop the detection area for motion. </br>
</br>

## Recommended Set up

</br>
- Pycharm IDE (very highly recommended)</br>
- Raspberry Pi with bluetooth connection (3 and above)</br>
- Database is optional but not required </br>
- Raspberry Pi Camera (Any model should work) </br>
NOTE: There will be a 5-7sec delay in video feed due to processing power of the raspberry pi </br>
</br>

## Alternate Setup

</br>
- Pycharm IDE </br>
- Laptop/Computer </br>
- Webcam (Different models may have different input lag. Worked optimally with Logitech C525. Logitech C922 had significant input lag) </br>
</br>

## To run

</br>
- Set up Raspberry Pi with sensors.</br>
- Make sure webcam / Raspberry Pi camera is installed and functional</br>
- If database is running, run "MotionDetectionWithDatabase.py", otherwise use "MotionDetectionWithoutDatabase.py"</br>
- Once running, an image will be taken by the camera and displayed to you. Select the area you want for motion Detection </br>
- Afterwards all images and livefeed streams will be shown to you:
  - Uncropped Image: Full unaltered video stream
  - Image: Motion Detection stream with blue boxes recognising movement</br>
  - Frame_Delta: Difference in the two frames (Taken a specified time apart. Default 0.25s)</br>
  - Threshold: Difference in two frames converted to pixels. One the pixel area is large enough, it will trigger detection</br>
- Once motion Detection is detected for a certain period of time (A counter is used within the code), it will state motion detected.
  </br>
  
  ## Notes
  
  </br>
  
  
