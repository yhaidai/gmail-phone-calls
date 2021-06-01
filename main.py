import time

from calls import make_call
from constants import PERSONAL_PHONE_NUMBER
from mail import message_from_epam

if __name__ == '__main__':
    while True:
        if message_from_epam():
            make_call(PERSONAL_PHONE_NUMBER)
            break

        time.sleep(2)
