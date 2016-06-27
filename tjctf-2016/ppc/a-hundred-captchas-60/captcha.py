#!/usr/bin/python3 -u

# You need figlet installed to run this script.
# You can use nc -lvp 1337 -e "./captcha.py" to run this script as a server.

import random
import string
import threading
import time
from subprocess import Popen, PIPE

letters = "234679abcdefghjkmnpqrstuvwyzABCDEFGHJKLMNPQRTUVWYZ"
timeout = 30
flag = open("flag.txt").read().strip()

def figlet(key):
    process = Popen(["figlet", "-m-1", key], stdout=PIPE)
    out, err = process.communicate()
    process.wait()
    return out.decode('utf8')

def checkcaptcha():
    print("Solve this captcha to continue:")
    key = ''.join(random.SystemRandom().choice(letters) for _ in range(8))
    print(figlet(key))
    return input('>>> ') == key

def main():
    print("To get the flag, solve a hundred captchas in", timeout, "seconds!")
    print("All captchas are alphanumeric characters.")

    startTime = time.time()
    for x in range(100):
        if not checkcaptcha():
            print("Wrong captcha! No flag for you. :(")
            exit()
        else:
            left = timeout - (time.time() - startTime)
            if left < 0:
                print("Time's up! No flag for you. :(")
                exit()
            print("Correct! You have", round(left, 1), "seconds left.")
        print()

    print("Nice! Your flag is: ", flag)

if __name__ == "__main__":
    main()
