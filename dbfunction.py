import mysql.connector

#Modular. Called in below functions to get latest number from column by id
def getNumber(column,table):
    mydb = mysql.connector.connect(
        user='root',
        password='password123',
        host='127.0.0.1',
        database='sensor_tag_data'
    )
    query = 'SELECT ' + column + ' FROM ' + table + ' ORDER BY id DESC LIMIT 1'
    c = mydb.cursor()
    c.execute(query)
    rows = c.fetchone()
    for row in rows:
        return row
    mydb.close()

def getPressure():
    pressure = getNumber('press','p_data') * 0.1
    pressure2dp = '{0:.2f}'.format(pressure)
    return str(pressure2dp) + ' kPa'

def getTemp():
    temp = getNumber('temp','t_data')
    temp2dp = '{0:.2f}'.format(temp)
    return str(temp2dp) + ' ' +'C'

def getHum():
    hum = getNumber('hum','t_data')
    hum2dp = '{0:.2f}'.format(hum)
    return str(hum2dp) + ' %RH'