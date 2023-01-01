import asyncio
from threading import Event, Thread
import time

from .Rover import *
from .Mongo import *
import src.Mongo as Mongo

def initRoverOnMongo(rover,dataCollection):
    Mongo.mongoConnectRoverBySerial(rover=rover,dataCollection=dataCollection)

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def data_streams(rover,dataCollection):
    print('Starting Listening to MongoDB.\n')
    exit_event = Event()

    print('Cleaning Loop Started.\n')
    clean_area_loop = asyncio.new_event_loop()
    clean_area_loop.call_soon_threadsafe(cleanArea,rover,dataCollection,exit_event)
    t = Thread(target=start_loop, args=(clean_area_loop,))
    t.start()
    time.sleep(0.25)

    print('Data Loop Started.\n')
    rover_data_loop = asyncio.new_event_loop()
    rover_data_loop.call_soon_threadsafe(Mongo.updateRoverData,dataCollection,rover)
    t = Thread(target=start_loop, args=(rover_data_loop,))
    t.start()
    time.sleep(0.25)

def cleanArea(rover, dataCollection,exit_event):
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

    

def mainStart(serial=None, connection=None,dataCollection=None):
    if serial != None:
        print(serial)
        rover = Rover(roverSerial=serial,connection=connection)
        initRoverOnMongo(rover=rover,dataCollection=dataCollection)
        data_streams(rover=rover, dataCollection=dataCollection)

if __name__ == '__main__':
    pass
else:
    mainStart()