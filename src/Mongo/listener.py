import time
from threading import Event, Thread
from ..util import keyboard_shutdown
from .setup import mongoUpdateRoverBySerial,mongoUpdateDroneStatus
from ..roverClean import roverUnDock,roverDock
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
                
                updated_roverStatus = document['fullDocument']['droneStatus']
                roverSerial = document['fullDocument']['serial']
                print("Change in rover status")
                print(updated_roverStatus)

                # if(document['fullDocument']['droneStatus']=="Free"):
                    # print("Edge case, Deal later")
                    
                if roverSerial == serial:
                    # if(mongoRoverStatus(drone=drone,roverDataCollection=roverDataCollection)=="Free"):
                    # if((drone.droneStatus=="Free") and updated_roverStatus=="Drop"):
                    if(updated_roverStatus=="Init"):
                        rover.roverStatus='Init'
                        print("Assumning Rover is inside Drone initially")
                        print("------------------Drop Rover---------------------")
                        mongoUpdateDroneStatus(rover,droneDataCollection=droneDataCollection,status="Drop")
                        # t = Thread(target=droneCleanDrop,
                        #         args=(drone,exit_event,droneDataCollection,roverDataCollection))
                        # # t = Thread(target=droneCleanDrop,
                        # #        args=(drone,exit_event,droneDataCollection,roverDataCollection=roverDataCollection))
                        # t.start()

                    elif(updated_roverStatus=="UnDock"):
                        print("Undock Rover")
                        print("------------------Undock Rover---------------------")
                        t = Thread(target=roverUnDock,
                                   args=(rover,roverDataCollection,droneDataCollection,exit_event))
                        t.start()

                    elif(updated_roverStatus=="Dock"):
                        print("Dock Rover")
                        print("------------------Dock Rover---------------------")
                        t = Thread(target=roverDock,
                                   args=(rover,roverDataCollection,droneDataCollection,exit_event))
                        t.start()
       
                    else:
                        pass
                    

                # elif updated_takeOffStatus == False and roverSerial == serial:
                #     print("-------------------Land------------------------")
                #     print("-> Start Landing Process")

                #     ##------> LAND THE DRONE

                #     # vehicle land function from drone class
                #     # drone.landDrone()
                #     # exit_event.set()
                #     # print("-> Exit Event Set")
                #     # t.join()
                #     pass
                    

    except KeyboardInterrupt:
        keyboard_shutdown()

