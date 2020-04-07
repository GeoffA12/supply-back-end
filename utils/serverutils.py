import os
# from dotenv import load_dotenv

ver = '0.4.0'


def connectToSQLDB():
    import mysql.connector as sqldb
    # password = os.getenv('DB_PASSWORD')
    password = 'password'
    return sqldb.connect(user='root', password=password, database='team22supply', port=6022)


def notifications(recipients, subject, body, sender='noreply@wego.com'):
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    
    # project_folder = os.path.expanduser('~/supply-backend/Experimenting')  # adjust as appropriate
    # load_dotenv(os.path.join(project_folder, '.env'))
    
    # SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SENDGRID_API_KEY = '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'
    
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
