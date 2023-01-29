from .util import keyboard_shutdown
import time
from .Mongo import * 
def roverUnDock(rover,roverDataCollection,droneDataCollection,exit_event):
    for i in range(5):
        time.sleep(1)
        print("UnDocking")

    print("UnDocked, now going to starting position")
    for i in range(5):
        time.sleep(1)
        print("Moving towards start location")
    print("Ready to clean")

    print("Sending drone back")
    mongoUpdateDroneStatus(rover=rover,droneDataCollection=droneDataCollection,status="waitAtHome")
    mongoUpdateRoverStatus(rover=rover,roverDataCollection=roverDataCollection,status="Cleaning")

    print("--------Start Cleaning-------")
    # Cleaning Algo called here
    print("Cleaning Complete")
    for i in range(5):
        time.sleep(1)
        print("Moving towards pickup location")
    print("Calling Drone to pickup")

    mongoUpdateDroneStatus(rover=rover,droneDataCollection=droneDataCollection,status="Pickup")
    mongoUpdateRoverStatus(rover=rover,roverDataCollection=roverDataCollection,status="Pickup")

    return

def roverDock(rover,roverDataCollection,droneDataCollection,exit_event):
    for i in range(5):
        time.sleep(1)
        print("Docking")

    print("Docked")
    print("Sending drone to next panel")

    # Go to next panel
    mongoUpdateDroneStatus(rover=rover,droneDataCollection=droneDataCollection,status="nextPanel")
    mongoUpdateRoverStatus(rover=rover,roverDataCollection=roverDataCollection,status="Busy")

    # Go back home
    mongoUpdateDroneStatus(rover=rover,droneDataCollection=droneDataCollection,status="goHome")
    mongoUpdateRoverStatus(rover=rover,roverDataCollection=roverDataCollection,status="Busy")

    return




def cleanArea(rover, roverDataCollection,droneDataCollection,exit_event):
    try:
        #Check if cleaning should start
        print('check drone status')
        rover.workingStatus = True
        rover.setupAndArm()
        rover.changeVehicleMode('GUIDED')
        print('Cleaning Started')
        #currently without ultrasonic sensor

        j = 0
        while j < 2:
            i = 0
            while i < 5:
                i = i + 1
                time.sleep(1)
                rover.moveForward(0.5)
            i = 0
            while i < 5:
                i = i + 1
                time.sleep(1)
                rover.moveBackward(0.5)
            rover.changeYaw(0.8)
            rover.moveForward(0.2)
            rover.changeYaw(-0.8)
            j = j + 1

        rover.workingStatus = False

    except KeyboardInterrupt:
        keyboard_shutdown()

   