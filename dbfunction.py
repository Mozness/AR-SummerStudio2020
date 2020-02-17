import mysql.connector

#Currently returns pressure from TI sensor. Will be modular when I can be bothered to do that
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
    return str(pressure) + ' kPa'

def getTemp():
    temp = getNumber('temp','t_data')
    return str(temp) + ' C'

def getHum():
    hum = getNumber('hum','t_data')
    return str(hum) + ' %RH'