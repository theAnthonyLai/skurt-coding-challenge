import json
import smtplib
import urllib.request
import time
from threading import Timer

from shapely.geometry import shape, Point, mapping

SKURT_API_URL = 'http://skurt-interview-api.herokuapp.com/carStatus/'
MAX_CAR_ID = 10
MIN_CAR_ID = 1

class sendEmail:
    def __init__(self, email, password, recipient):
        self.email = email
        self.password = password
        self.recipient = recipient

    def send(self, subject, body):
        
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
            print("Email sent successfully!")
        except Exception as e:
            print(e)


def checkCarStatus(carId, emailSender, emailFormat):
    print('Checking car %d' % carId)
    #testVar = SKURT_API_URL + str(carId)
    #print(testVar)
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
            print('Car %d out of boundary' % carId)

    except Exception as e:
            print(e)


def checkCarThread(carId, emailSender, emailFormat):
    # check current car
    checkCarStatus(carId, emailSender, emailFormat)

    carId += 1
    if carId > MAX_CAR_ID:
        carId = MIN_CAR_ID

    Timer(5.0, checkCarThread, (carId, emailSender, emailFormat)).start()
    print('EVENT:', time.time())
    #emailSender.send(emailFormat['subject'], emailFormat['body'])


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

    # try:
    #     f = urllib.request.urlopen(SKURT_API_URL + '10')
    #     text = f.read().decode('utf-8')
    #     #print(text)
    #     #print(type(text))

    #     obj = json.loads(text)
    #     #print(type(obj))
    #     #print(obj)
    #     #print(obj['features'][1]['geometry'])

    #     boundary = shape(obj['features'][1]['geometry'])
    #     #print(json.dumps(mapping(boundary)))
    #     carLoc = Point(obj['features'][0]['geometry']['coordinates'][0], obj['features'][0]['geometry']['coordinates'][1])

    #     # Returns True if the boundary and interior of the object intersect in any way with those of the other.
    #     if boundary.intersects(carLoc):
    #         print('Car within boundary')
    #     else:
    #         print('Car out of boundary')

    # except Exception as e:
    #         print(e)

if __name__ == "__main__":
    main()