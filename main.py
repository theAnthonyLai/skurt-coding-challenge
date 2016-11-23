import json
import smtplib
import urllib.request
import datetime
from threading import Timer
from shapely.geometry import shape, Point, mapping

SKURT_API_URL = 'http://skurt-interview-api.herokuapp.com/carStatus/'
MAX_CAR_ID = 10
MIN_CAR_ID = 1
MONITOR_INTERVAL = 5 # (seconds) TODO

class sendEmail:
    def __init__(self, email, password, recipient):
        self.email = email
        self.password = password
        self.recipient = recipient

    def send(self, subject, body, carId):
        msg = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (self.email, self.recipient, subject, body)

        try:
            # need SMTP_SSL for port 465
            server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            # initiate SMTP conversation with SMTP server
            server_ssl.ehlo()
            # provide log-in info
            server_ssl.login(self.email, self.password)
            server_ssl.sendmail(self.email, self.recipient, msg)
            server_ssl.close()
            print('Alert email for car %d sent successfully!' % carId)
        except Exception as e:
            print(e)


def checkCarStatus(carId, emailSender, emailFormat):
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
            emailSender.send(emailFormat['subject'], emailFormat['body'], carId)

    except Exception as e:
            print('Err getting car status:', e)


def checkCarThread(carId, emailSender, emailFormat):
    # check current car
    print('================================')
    print('EVENT:', datetime.datetime.now())
    checkCarStatus(carId, emailSender, emailFormat)

    carId += 1
    if carId > MAX_CAR_ID:
        carId = MIN_CAR_ID

    Timer(MONITOR_INTERVAL, checkCarThread, (carId, emailSender, emailFormat)).start()


def main():
    print("Hello World")

    # load json credentials and alert email format
    with open('credentials.json') as credentials_file:
        credentials = json.load(credentials_file)
    with open('emailFormat.json') as emailFormat_file:
        emailFormat = json.load(emailFormat_file)

    emailSender = sendEmail(credentials['username'], credentials['password'], emailFormat['recipient'])
    #emailSender.send(emailFormat['subject'], emailFormat['body'])


    checkCarThread(MIN_CAR_ID, emailSender, emailFormat)

if __name__ == "__main__":
    main()