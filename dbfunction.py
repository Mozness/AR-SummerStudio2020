import mysql.connector
import csv

# Exports a table to CSV
def exportCSV(table):
    mydb = mysql.connector.connect(
        user='root',
        password='password123',
        host='127.0.0.1',
        database='sensor_tag_data'
    )
    query = 'SELECT * FROM ' + table
    c = mydb.cursor()
    c.execute(query)
    result = c.fetchall()
    export = csv.writer(open('/Users/micha/Desktop/' + table +'dump.csv', 'w'))
    for x in result:
        export.writerow(x)
    mydb.close()

# Function that clears all data from a specified table except the last entry
def clearTable(table):
    mydb = mysql.connector.connect(
        user='root',
        password='password123',
        host='127.0.0.1',
        database='sensor_tag_data'
    )
    query = 'DELETE FROM ' + table + ' WHERE id not in (SELECT id FROM (SELECT id FROM ' + table + ' ORDER BY id DESC LIMIT 1)foo)'
    c = mydb.cursor()
    c.execute(query)
    mydb.commit()

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