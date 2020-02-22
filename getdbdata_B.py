import mysql.connector
import datetime

def dbconnect():
    mydb = mysql.connector.connect(
        user='remote_user',
        password='password123',
        host='127.0.0.1',
        database='tag_data'
    )
    return mydb

def getdataset(table, lim, c_num=2):
    mydb = dbconnect()
    query = 'SELECT * FROM {} ORDER BY id DESC LIMIT {}'.format(table, lim)
    c = mydb.cursor()
    c.execute(query)
    rows = c.fetchall()
    time = []
    data_v = []
    for row in rows:
        time.insert(0, datetime.datetime.strftime(row[1], '%H:%M:%S'))
        data_v.insert(0, row[c_num])
    return time, data_v
    mydb.close()

def getNumber(column,table):
    mydb = dbconnect()
    query = 'SELECT {} FROM {} ORDER BY id DESC LIMIT 1'.format(column, table)
    c = mydb.cursor()
    c.execute(query)
    rows = c.fetchone()
    for row in rows:
        return row
    mydb.close()

def getPressure():
    pressure = getNumber('press','p_data')
    # pressure2dp = '{0:.2f}'.format(pressure)
    pressure2dp = int(pressure)
    return str(pressure2dp) + ' kPa'

def getTemp():
    temp = getNumber('temp','t_data')
    temp2dp = '{0:.2f}'.format(temp)
    return str(temp2dp) + ' ' +'C'

def getWTemp():
    temp = getNumber('w_temp','w_data')
    temp2dp = '{0:.2f}'.format(temp)
    return str(temp2dp) + ' ' +'C'

def getHum():
    hum = getNumber('hum','t_data')
    hum2dp = '{0:.2f}'.format(hum)
    return str(hum2dp) + ' %RH'