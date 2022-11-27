import time

from ..util import keyboard_shutdown
from .setup import mongoUpdateRoverBySerial

def updateRoverData(dataCollection,rover):
    try:
        while True:
            print("Updating Drone")
            mongoUpdateRoverBySerial(rover,dataCollection)
            print(rover.serial)
            time.sleep(5)
    except KeyboardInterrupt:
        keyboard_shutdown()