from dotenv import load_dotenv

load_dotenv()
ver = '0.1.0'


def connectToSQLDB():
    import os
    import mysql.connector as sqldb
    password = os.getenv('DB_PASSWORD')
    return sqldb.connect(user='root', password=password, database='team22supply', port=6022, buffered=True)


def getCourierCandidates(data):
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor(buffered=True)

    statement = '''SELECT vid, licenseplate,
                make, model, current_lat, current_lon
                FROM vehicles, fleets
                WHERE vehicles.status = %s AND type = %s
                AND vehicles.fleetid = fleets.fleetid'''
    cursor.execute(statement, tuple(data))
    vehicleEntries = cursor.fetchall()

    cursor.close()
    sqlConnection.close()

    return vehicleEntries


def updateVehicleStatus(vid):
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor(buffered=True)

    statement = 'UPDATE vehicles SET status = 1 where vid = %s'
    cursor.execute(statement, (vid,))
    sqlConnection.commit()

    cursor.close()
    sqlConnection.close()


def storeDispatch(dispatchData):
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor(buffered=True)

    statement = 'INSERT INTO dispatch VALUES (Null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(statement, dispatchData)
    sqlConnection.commit()

    cursor.close()
    sqlConnection.close()


def addVehicle(vehicleData):
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor(buffered=True)

    statement = 'INSERT INTO vehicles VALUES (Null, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.executemany(statement, vehicleData)
    sqlConnection.commit()

    cursor.close()
    sqlConnection.close()


def delVehicle(vehicleData):
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor(buffered=True)

    statement = 'DELETE FROM vehicles WHERE vid = %s'
    cursor.executemany(statement, vehicleData)
    sqlConnection.commit()

    cursor.close()
    sqlConnection.close()


def updVehicle(statement, vehicleData):
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor(buffered=True)

    cursor.execute(statement, tuple(vehicleData))
    sqlConnection.commit()

    cursor.close()
    sqlConnection.close()


def getFMID(emailOrUser):
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor(buffered=True)

    statement = 'SELECT fmid FROM fleetmanagers WHERE email = %s OR username = %s'
    data = (emailOrUser, emailOrUser,)
    cursor.execute(statement, data)
    fmid = cursor.fetchone()[0]

    cursor.close()
    sqlConnection.close()

    return fmid


def addFleet(fleetData):
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor(buffered=True)

    statement = 'INSERT INTO fleets VALUES (Null, %s, %s, %s)'
    cursor.execute(statement, fleetData)
    sqlConnection.commit()

    cursor.close()
    sqlConnection.close()


def getVehicleByVID(vid):
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor(buffered=True)

    statement = 'SELECT * FROM vehicles WHERE vid = %s'
    cursor.execute(statement, (vid,))
    entry = cursor.fetchone()[0]

    cursor.close()
    sqlConnection.close()

    return entry


def getAllVehicles():
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor(buffered=True)

    statement = 'SELECT * FROM vehicles'
    cursor.execute(statement)
    rows = cursor.fetchall()

    cursor.close()
    sqlConnection.close()

    return rows


def getFleetIDByFMCredentials(users):
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor(buffered=True)

    statement = '''SELECT fleets.fleetid
                   FROM fleets, fleetmanagers
                   WHERE fleets.fmid = fleetmanagers.fmid
                   AND (fleetmanagers.username = %s
                   OR fleetmanagers.email = %s)'''
    fleetIDs = []
    for user in users:
        cursor.execute(statement, user)
        temp = cursor.fetchall()
        flatten = [item for sublist in temp for item in sublist]
        print(flatten)
        fleetIDs.extend(flatten)
        print(fleetIDs)

    cursor.close()
    sqlConnection.close()

    return fleetIDs


def getAllFleets():
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor(buffered=True)

    statement = 'SELECT * FROM fleets'
    cursor.execute(statement)
    rows = cursor.fetchall()

    cursor.close()
    sqlConnection.close()

    return rows


def getDispatchByVID(vids):
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor()

    statement = '''SELECT * FROM dispatch WHERE vid = %s'''
    print(statement)
    dispatches = []
    for vid in vids:
        cursor.execute(statement, vid)
        dispatchTup = cursor.fetchall()
        print('tup:', dispatchTup)
        if dispatchTup is not None:
            temp = [list(x) for x in dispatchTup]
            dispatches.extend(temp)

    cursor.close()
    sqlConnection.close()

    return dispatches
