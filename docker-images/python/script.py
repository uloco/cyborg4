from lib import lib
import time

print("Hello World")
lib.helloLib()

counter = 0

while(counter < 5):
    print("I run")
    time.sleep(0.1)
    counter += 1
