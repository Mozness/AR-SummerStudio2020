import MySQLdb
import csv
import datetime

# Connects to Database. Change the name of the user and database to your db
def dbconnect():
    mydb = MySQLdb.connect(
        user='root',
        password='password123',
        host='127.0.0.1',
        database='sensor_tag_data'
    )
    return mydb

# Gets dataset for Dash components
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

# Exports a table to CSV
def exportCSV(table):
    mydb = dbconnect()
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
    mydb =dbconnect()
    query = 'DELETE FROM ' + table + ' WHERE id not in (SELECT id FROM (SELECT id FROM ' + table + ' ORDER BY id DESC LIMIT 1)foo)'
    c = mydb.cursor()
    c.execute(query)
    mydb.commit()

#Modular. Called in below functions to get latest number from column by id
def getNumber(column,table):
    mydb = dbconnect()
    query = 'SELECT ' + column + ' FROM ' + table + ' ORDER BY id DESC LIMIT 1'
    c = mydb.cursor()
    c.execute(query)
    rows = c.fetchone()
    for row in rows:
        return row
    mydb.close()

# Gets pressure
def getPressure():
    pressure = getNumber('press','p_data') * 0.1
    pressure2dp = '{0:.2f}'.format(pressure)
    return str(pressure2dp) + ' kPa'

# Gets Temperature (from sensor tag)
def getTemp():
    temp = getNumber('temp','t_data')
    temp2dp = '{0:.2f}'.format(temp)
    return str(temp2dp) + ' ' +'C'

# Gets Water temp
def getWTemp():
    temp = getNumber('w_temp','w_data')
    temp2dp = '{0:.2f}'.format(temp)
    return str(temp2dp) + ' ' +'C'

# Gets humidity (from sensor tag)
def getHum():
    hum = getNumber('hum','t_data')
    hum2dp = '{0:.2f}'.format(hum)
    return str(hum2dp) + ' %RH'

# Gets boolean boil status
def getBoil():
    boil = getNumber('boil', 'boil_status')
    if boil == 1:
        return "Water is boiling"
    else:
        return "Water is not boiling"

# Gets boolean water status
def getLevel():
    #lvl = getNumber('boil', 'water_low')
    lvl = 1
    if lvl == '1':
        return "Water is low"
    else:
        return "Enough water"