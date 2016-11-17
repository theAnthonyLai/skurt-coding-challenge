import json
import smtplib
import urllib.request

SKURT_API_URL = 'http://skurt-interview-api.herokuapp.com/carStatus/'

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


def main():
    print("Hello World")

    # load json credentials and alert email format
    with open('credentials.json') as credentials_file:
        credentials = json.load(credentials_file)
    with open('emailAlert.json') as emailAlert_file:
        emailAlert = json.load(emailAlert_file)

    #emailSender = sendEmail(credentials['username'], credentials['password'], emailAlert['recipient'])
    #emailSender.send(emailAlert['subject'], emailAlert['body'])

    try:
        f = urllib.request.urlopen(SKURT_API_URL + '5')
        text = f.read().decode('utf-8')
        #print(text)
        print(type(text))

        obj = json.loads(text)
        print(type(obj))
        print(obj)


    except Exception as e:
            print(e)

if __name__ == "__main__":
    main()