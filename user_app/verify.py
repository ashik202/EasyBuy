import os
from decouple import config
from twilio.rest import Client
from django.conf import settings

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def sentOTP(mobile):
    phone = "+91" + str(mobile)
    account_sid = config('account_sid')
    auth_token = config('auth_token')
    client = Client(account_sid, auth_token)

    verification = client.verify.services(
        config('services')
    ).verifications.create(to=phone, channel="sms")

    print(verification.status)


def checkOTP(mobile, otp):
    account_sid = 'AC573613fb2dc222493bdf88058d34aa90'
    auth_token = '08c71ba55eae23bef14c83c311107036'
    client = Client(account_sid, auth_token)

    verification_check = client.verify.services(
        'VA79eac7c63117259ffea50c79e1c16178'
    ).verification_checks.create(to="+91" + mobile, code=otp)

    print(verification_check.status)
    if verification_check.status == "approved":
        return True
    else:
        return False