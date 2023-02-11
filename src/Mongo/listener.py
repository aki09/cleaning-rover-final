import time
from threading import Event, Thread
from ..util import keyboard_shutdown
from .setup import mongoUpdateRoverBySerial,mongoUpdateDroneStatusBySerial

def updateRoverData(dataCollection,rover):
    try:
        while True:
            print("Updating Drone")
            mongoUpdateRoverBySerial(rover,dataCollection)
            print(rover.serial)
            time.sleep(5)
    except KeyboardInterrupt:
        keyboard_shutdown()


def listenerMongoData(rover,roverDataCollection,droneDataCollection,exit_event):
    print("Mongo Listner Started")
    serial=rover.serial


    pipelineRoverStatus = [{
        '$match': {
            '$and': [
                {"updateDescription.updatedFields.roverStatus": {'$exists': True}},
                {'operationType': "update"}]
        }
    }]
    
    try:
        for document in roverDataCollection.watch(pipeline=pipelineRoverStatus, full_document='updateLookup'):
            if document['fullDocument']['serial'] == serial:
                
                updated_roverStatus = document['fullDocument']['roverStatus']
                roverSerial = document['fullDocument']['serial']
                print("Change in rover status")
                print(updated_roverStatus)
                if roverSerial == serial:
                    rover.handle_rover_status(updated_roverStatus,droneDataCollection,roverDataCollection,exit_event)

    except KeyboardInterrupt:
        keyboard_shutdown()

