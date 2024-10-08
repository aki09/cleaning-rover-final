import asyncio
from threading import Event, Thread
import time

from .Rover import *
from .Mongo import *
import src.Mongo as Mongo

def initRoverOnMongo(rover,roverDataCollection):
    Mongo.mongoConnectRoverBySerial(rover=rover,roverDataCollection=roverDataCollection)

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def data_streams(rover,roverDataCollection,droneDataCollection):
    print('Starting Listening to MongoDB.\n')
    exit_event = Event()

    # print('Cleaning Loop Started.\n')
    # clean_area_loop = asyncio.new_event_loop()
    # clean_area_loop.call_soon_threadsafe(cleanArea,rover,roverDataCollection,droneDataCollection,exit_event)
    # t = Thread(target=start_loop, args=(clean_area_loop,))
    # t.start()
    # time.sleep(0.25)

    update_loop = asyncio.new_event_loop()
    update_loop.call_soon_threadsafe(listenerMongoData,rover,roverDataCollection,droneDataCollection,exit_event)
    t = Thread(target=start_loop, args=(update_loop,))
    t.start()
    time.sleep(0.25)

    print('Data Loop Started.\n')
    rover_data_loop = asyncio.new_event_loop()
    rover_data_loop.call_soon_threadsafe(Mongo.updateRoverData,roverDataCollection,rover)
    t = Thread(target=start_loop, args=(rover_data_loop,))
    t.start()
    time.sleep(0.25)


def mainStart(serial=None, connection=None,roverDataCollection=None,droneDataCollection=None):
    if serial != None:
        print(serial)
        rover = Rover(roverSerial=serial,connection=connection)
        initRoverOnMongo(rover=rover,roverDataCollection=roverDataCollection)
        data_streams(rover=rover, roverDataCollection=roverDataCollection,droneDataCollection=droneDataCollection)

if __name__ == '__main__':
    pass
else:
    mainStart()