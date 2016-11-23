import json
import smtplib
import urllib.request
import datetime
from threading import Timer
from shapely.geometry import shape, Point, mapping
from enum import Enum

EMAIL_SERVER_URL = 'smtp.gmail.com'
EMAIL_SERVER_PORT = 465
SKURT_API_URL = 'http://skurt-interview-api.herokuapp.com/carStatus/'
MAX_CAR_ID = 10
MIN_CAR_ID = 1
MONITOR_INTERVAL = 25 # seconds (300 seconds / 10 cars; give some extra time in case email server is slow)

class EmailType(Enum):
    test = 1
    alert = 2
    error = 3

class SendEmail:
    def __init__(self, email, password, recipient, format):
        self.email = email
        self.password = password
        self.recipient = recipient
        self.format = format

    def send(self, type, carId = -1):
        if type == EmailType.test:
            # for default test email, no carId
            msg = """From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (self.email, self.recipient, self.format[type.name]['subject'], self.format[type.name]['body'])
        else:
            # add carId to email subject line
            msg = """From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (self.email, self.recipient, self.format[type.name]['subject'] % carId, self.format[type.name]['body'])

        try:
            # need SMTP_SSL for port 465
            server_ssl = smtplib.SMTP_SSL(EMAIL_SERVER_URL, EMAIL_SERVER_PORT)
            # initiate SMTP conversation with SMTP server
            server_ssl.ehlo()
            # provide log-in info
            server_ssl.login(self.email, self.password)
            server_ssl.sendmail(self.email, self.recipient, msg)
            server_ssl.close()
            if type == EmailType.test:
                print('Test email has been sent out successfully! Begin checking each car.')
            elif type == EmailType.alert:
                print('Alert email for car %d sent successfully!' % carId)
            else:
                print('Error email for car %d sent successfully!' % carId)
        except Exception as e:
            print(e)


def checkCarStatus(carId, emailSender):
    print('Checking car %d' % carId)

    try:
        res = urllib.request.urlopen(SKURT_API_URL + str(carId))
        text = res.read().decode('utf-8')
        obj = json.loads(text)

        boundary = shape(obj['features'][1]['geometry'])
        carLoc = Point(obj['features'][0]['geometry']['coordinates'][0], obj['features'][0]['geometry']['coordinates'][1])

        # Returns True if the boundary and interior of the object intersect in any way with those of the other.
        if boundary.intersects(carLoc):
            print('Car %d within boundary' % carId)
        else:
            print('Car %d out of boundary. Sending alert email.' % carId)
            emailSender.send(EmailType.alert, carId)

    except Exception as e:
            print('Err getting car status:', e)
            emailSender.send(EmailType.error, carId)


def checkCarThread(carId, emailSender):
    # check current car
    print('================================')
    print('EVENT:', datetime.datetime.now())
    checkCarStatus(carId, emailSender)

    carId += 1
    if carId > MAX_CAR_ID:
        carId = MIN_CAR_ID

    Timer(MONITOR_INTERVAL, checkCarThread, (carId, emailSender)).start()


def main():
    print("Setting up login credentials.")

    # load json credentials and alert email format
    with open('credentials.json') as credentials_file:
        credentials = json.load(credentials_file)
    with open('emailFormat.json') as emailFormat_file:
        emailFormat = json.load(emailFormat_file)

    emailSender = SendEmail(credentials['username'], credentials['password'], emailFormat['recipient'], emailFormat['format'])

    print("Sending one test email to verify the receipt of alert email.")
    emailSender.send(EmailType.test)

    # fire up checkCarThread to repeatedly checking each car
    checkCarThread(MIN_CAR_ID, emailSender)

if __name__ == "__main__":
    main()