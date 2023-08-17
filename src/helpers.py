import sys
import time

WAIT_TIME = 45  # time in seconds


def wait(sec):
    # output the . -> .. -> ... waiting loop animation
    for j in range(sec):
        print('.', end='')
        sys.stdout.flush()
        time.sleep(1)
    # clear the terminal line
    print('\r', end='')
    print('                                                   ', end='\r')
    time.sleep(1)
