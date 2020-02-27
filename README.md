# AR-SummerStudio2020
</br>
Motion sensing code must be run separately from main code. </br>
This AR program was built in Pycharm. Run the video-drawing class to run the program. </br>
Any unused classes are kept for the purpose of documentation.</br>
node-red_final.json is a node-red flow used for updating the sensors on the Raspberry Pis. Run it in node red.</br>
You'll need to set up your own MySQL database as well and modify the node-red flow and code where appropriate.</br>
</br>
## Recommended Set up ##
</br>
- Pycharm IDE (very highly recommended)</br>
- Raspberry Pi with bluetooth connection (3 and above)</br>
- Texas Instruments CC2650 Sensor Tag</br>
- DS18B20 waterproof temperature sensor</br>
- Windows PC with My SQL C libraries installed. Best installed with whole MySQL package (especially if you chose to use a local database). This is because a C based connector is used in the program that privides better performance in the connection with the database than the Python connector.</br>
- MySQL database. Currently the program is configured to a local database. Node Red flow will need to be updated with new Ip and name of your database.</br>
- Second webcam for motion sensor highly recommended. Another from primary AR feed also ighly recommended but not needed to run program.</br>
- Make sure all packages in PyCharm are installed.</br>
</br>
## To run ##
</br>
- Set up Raspberry Pi with sensors.</br>
- Change Node Red flow to connect to your database and update your tables.</br>
- Start MySQL server and run Pis. Data should update if set up correctly.</br>
- Run video-drawing.py on Pycharm to launch program.</br>
- Run motion sensing program.
