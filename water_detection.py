#!/usr/bin/python

import spidev
import time
import mysql.connector

#set delay
delay = 0.5
pressure_pad = 0

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=1000000

counter = 0
def sendtodb(contact):
    mydb = mysql.connector.connect(user = 'remoteuser', password = 'password123', host = "172.19.204.21", database='sensor_tag_data', use_pure=True)
    
    query = "INSERT INTO water_low (datetime, w_low) VALUE (NOW(), "+ contact +")"
    c = mydb.cursor()
    c.execute(query)
    mydb.commit()
    
    mydb.close()
    


def readadc(adcnum):
    #read data from MCP3008
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

# try:
while True:
    pressure_value = readadc(pressure_pad) #resistance to pressure
    print("Pressure Value is: %d" %pressure_value)
    
    if pressure_value <400:

        counter = counter -1

        
        
    else:

        counter = counter + 1

        
            
    if counter >=10:
        print("Water high")
        
        if counter > 10:
            counter = 6
            sendtodb("1")
            
        else:
            sendtodb("1")
            pass
    elif counter <5:
        if counter <0:
            sendtodb("0")
            print("Water Low")
            
        else:
            sendtodb("0")
            print("Water Low")
            
    
    time.sleep(delay)
