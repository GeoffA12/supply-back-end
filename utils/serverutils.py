import os
from dotenv import load_dotenv
import threading
from datetime import datetime
import time

ver = '0.4.0'

# project_folder = os.path.expanduser('~/supply-backend/utils')  # adjust as appropriate
# print(os.path)
load_dotenv()


def connectToSQLDB():
    import mysql.connector as sqldb
    password = os.getenv('DB_PASSWORD')
    # password = 'password'
    # print(f'Password: {password}')
    return sqldb.connect(user='root', password=password, database='team22supply', port=6022, buffered=True)


def notifications(recipients, subject, body, sender='noreply@wego.com'):
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    print(sender)
    print(recipients)
    print(subject)
    print(body)

    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    # SENDGRID_API_KEY = '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'

    message = Mail(
            from_email=sender,
            to_emails=recipients,
            subject=subject,
            html_content=body)
    try:
        sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


def healthChecker():
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor()
    statement = 'SELECT fleetid, fmid FROM fleets;'
    cursor.execute(statement)
    rows = cursor.fetchall()
    cursor.close()
    sqlConnection.close()
    print(rows)
    for fleetData in rows:
        thread = threading.Thread(target=heartbeatListener, args=fleetData)
        thread.start()


def heartbeatListener(fleetid, fmid):
    print(f'Listener for Fleet {fleetid} has started')
    sqlConnection = connectToSQLDB()
    cursor = sqlConnection.cursor(buffered=True)

    statement = "SELECT email FROM fleetmanagers WHERE fmid = %s"
    cursor.execute(statement, (fmid,))
    email = cursor.fetchone()[0]
    cursor.close()
    sqlConnection.close()
    CHECKER_INTERVAL = 45
    missedHeartbeats = {}
    try:
        while True:
            time.sleep(CHECKER_INTERVAL)
            sqlConnection = connectToSQLDB()
            cursor = sqlConnection.cursor(buffered=True)

            statement = "SELECT vid, last_heartbeat FROM vehicles WHERE fleetid = %s AND status <> 3"
            cursor.execute(statement, (fleetid,))
            rows = cursor.fetchall()
            print(rows)
            cursor.close()
            sqlConnection.close()

            d = {k: v for (k, v) in rows}
            for vid, lasthb in d.items():
                if lasthb is not None:
                    now = datetime.now()
                    differenceAsDateTime = now - lasthb
                    difference = now - differenceAsDateTime
                    seconds = difference.total_seconds()
                    minutes = divmod(seconds, 60)[0]
                    print(f'Difference in minutes: {round(minutes, 4)}')
                    if minutes > 5.0000:
                        print(f'Vehicle ID: {vid} hasn\'t reported in for at least 5 minutes!')

                        subject = f'Vehicle ID: {vid} hasn\'t reported in for {round(minutes, 2)}'
                        body = f'Vehicle ID: {vid} hasn\'t reported in for {round(minutes, 2)}'
                        # notifications(recipients=email,
                        #               subject=subject,
                        #               body=body)
                else:
                    print('vehicle just added and hasn\'t spun up a heartbeat')
                    # notifications(recipients=email, subject='hi', body='hi')

    except KeyboardInterrupt:
        raise
    finally:
        print(f'Listener for Fleet {fleetid} is ending')
