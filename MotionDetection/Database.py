import mysql.connector
import csv
import datetime


def dbsend(isBoil):
    mydb = mysql.connector.connect(
        user='remoteuser',
        password='password123',
        host='172.19.112.112',
        database='sensor_tag_data',
        use_pure= True
    )

    query = "INSERT INTO boil_status (datetime, boil) VALUES (NOW(), "+ isBoil +")"
    c = mydb.cursor()
    c.execute(query)
    mydb.commit()


    mydb.close()
    #print(mydb)

dbsend("0")

def printDB():
    mydb = mysql.connector.connect(
        user='remoteuser',
        password='password123',
        host='172.19.112.112',
        database='sensor_tag_data',
        use_pure=True
    )
    print(mydb)

printDB()
