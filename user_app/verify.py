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
    account_sid = config('account_sid')
    auth_token = config('auth_token')
    client = Client(account_sid, auth_token)

    verification_check = client.verify.services(
        config('services')
    ).verification_checks.create(to="+91" + mobile, code=otp)

    print(verification_check.status)
    if verification_check.status == "approved":
        return True
    else:
        return False