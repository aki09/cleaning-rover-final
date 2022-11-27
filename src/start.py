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

    rover_data_loop = asyncio.new_event_loop()
    rover_data_loop.call_soon_threadsafe(Mongo.updateRoverData,dataCollection,rover)
    t = Thread(target=start_loop, args=(rover_data_loop,))
    t.start()
    time.sleep(0.25)

def cleanArea(rover, dataCollection):
    rover.workingStatus = True
    print('start')
    

def mainStart(serial=None, connection=None,dataCollection=None):
    if serial != None:
        print(serial)
        rover = Rover(roverSerial=serial,connection=connection)
        initRoverOnMongo(rover=rover,dataCollection=dataCollection)
        data_streams(rover=rover, dataCollection=dataCollection)
        cleanArea(rover=rover, dataCollection=dataCollection)

if __name__ == '__main__':
    pass
else:
    mainStart()