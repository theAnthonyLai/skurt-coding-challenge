# skurt-coding-challenge
A Python 3 script for the [Skurt Coding Challenge](https://github.com/theAnthonyLai/skurt-coding-challenge/blob/master/requirement.pdf). This script will make API calls to http://skurt-interview-api.herokuapp.com/carstatus/{CarID} repeatedly and alert via email within 5 minutes whenever a car goes out of bound.

## Setup

#### Shapely
The script uses [shapely](https://pypi.python.org/pypi/Shapely) to determine whether the cars are still in bound.
To install shapely:
```
pip install shapely
```

#### Credentials
A `credentials.json` file is needed to run the script. Please edit the username and password for the sender's account. If a non-gmail account is used, the `EMAIL_SERVER_URL` variable in `main.py` (line 9) will have to be changed.

#### Email Format
The email formats are defined in `emailFormat.json`
* `test` is for a test email that the script will send out in the beginning to verify the credentials and that the alert system is working
* `alert` is for the actual alert emails that will be sent by the script whenever a car is out of bound. `%d` is needed in the subject because the script will pass in the `CarID`
* `error` is the email that will be sent whenever the API request returns an error. `%d` is required in the subject as well

#### Recipient
The recipient email address is defined in `emailFormat.json`

### Usage
```
python3 main.py
```
The script will first send out a test email verifying the credentials provided in `credentials.json` and the recipient's email provided in `emailFormat.json`. Once the email is successfully sent, it will repeatedly make API calls to check all cars and send out an alert email with the `CarID` whenever a car is out of bound. If the API request fails, it will send out an error email with the `CarID`.
