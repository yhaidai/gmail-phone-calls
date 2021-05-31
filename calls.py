from twilio.rest import Client

from constants import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, \
    PERSONAL_PHONE_NUMBER, TWILIO_PHONE_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def make_call(phone_to: str):
    call = client.calls.create(
        twiml='<Response><Say>Hello, World!</Say></Response>',
        to=phone_to,
        from_=TWILIO_PHONE_NUMBER
    )
    print(call.sid)


if __name__ == '__main__':
    make_call(PERSONAL_PHONE_NUMBER)
