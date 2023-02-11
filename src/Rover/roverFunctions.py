from threading import Event, Thread
from ..util import keyboard_shutdown
import src.Mongo as Mongo
import time


def free(rover):
    print("Rover is free.")
    return

def init(rover,droneDataCollection,DroneStatus,RoverStatus):
    print("Rover is initializing.")
    rover.roverStatus=RoverStatus.INIT
    print("Assumning Rover is inside Drone initially")
    print("------------------Drop Rover---------------------")
    Mongo.mongoUpdateDroneStatusBySerial(rover,droneDataCollection=droneDataCollection,statusValue=DroneStatus.DOCK)
    return 

def dock(rover,roverDataCollection,droneDataCollection,DroneStatus,RoverStatus,exit_event):
    print("Rover is docking.")
    print("------------------Dock Rover---------------------")
    t = Thread(target=roverDock,
                args=(rover,roverDataCollection,droneDataCollection,DroneStatus,RoverStatus,exit_event))
    t.start()
    return 

def undock(rover,roverDataCollection,droneDataCollection,DroneStatus,RoverStatus,exit_event):
    print("Rover is undocking.")
    print("------------------Undock Rover---------------------")
    t = Thread(target=roverUnDock,
                args=(rover,roverDataCollection,droneDataCollection,DroneStatus,RoverStatus,exit_event))
    t.start()
    return 

def busy(self):
    print("Rover is busy.")
    return 

def cleaning(self):
    print("Rover is cleaning.")
    return 

def pickup(self):
    print("Rover is picking up.")
    return 

def unknown_status(self):
    print("Unknown rover status.")
    return 

def roverUnDock(rover,roverDataCollection,droneDataCollection,DroneStatus,RoverStatus,exit_event):
    for i in range(5):
        time.sleep(1)
        print("UnDocking")

    print("UnDocked, now going to starting position")
    for i in range(5):
        time.sleep(1)
        print("Moving towards start location")
    print("Ready to clean")

    print("Sending drone back")
    Mongo.mongoUpdateDroneStatusBySerial(rover=rover,droneDataCollection=droneDataCollection,statusValue=DroneStatus.WAIT_AT_HOME)
    rover.roverStatus=RoverStatus.CLEANING
    Mongo.mongoUpdateRoverBySerial(rover=rover,roverDataCollection=roverDataCollection)

    print("--------Start Cleaning-------")
    # Cleaning Algo called here
    print("Cleaning Complete")
    for i in range(5):
        time.sleep(1)
        print("Moving towards pickup location")
    print("Calling Drone to pickup")

    Mongo.mongoUpdateDroneStatusBySerial(rover=rover,droneDataCollection=droneDataCollection,statusValue=DroneStatus.PICKUP)
    rover.roverStatus=RoverStatus.PICKUP
    Mongo.mongoUpdateRoverBySerial(rover=rover,roverDataCollection=roverDataCollection)

    return

def roverDock(rover,roverDataCollection,droneDataCollection,DroneStatus,RoverStatus,exit_event):
    for i in range(5):
        time.sleep(1)
        print("Docking")

    print("Docked")
    print("Sending drone to next panel")

    # Go to next panel
    Mongo.mongoUpdateDroneStatusBySerial(rover=rover,droneDataCollection=droneDataCollection,statusValue=DroneStatus.NEXT_PANEL)
    rover.roverStatus=RoverStatus.BUSY
    Mongo.mongoUpdateRoverBySerial(rover=rover,roverDataCollection=roverDataCollection)

    # Go back home
    Mongo.mongoUpdateDroneStatusBySerial(rover=rover,droneDataCollection=droneDataCollection,statusValue=DroneStatus.GO_HOME)
    rover.roverStatus=RoverStatus.BUSY
    Mongo.mongoUpdateRoverBySerial(rover=rover,roverDataCollection=roverDataCollection)

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

   