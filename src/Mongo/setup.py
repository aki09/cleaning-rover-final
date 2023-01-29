import pymongo

def mongoConnect(mongoUrl,database,collection):
    mc = pymongo.MongoClient(mongoUrl)
    mydb = mc[database]
    dataCollection = mydb[collection]
    return dataCollection

def mongoConnectRoverBySerial(rover,roverDataCollection):
    if roverDataCollection.find_one({'serial': rover.serial}):
        mongoUpdateRoverBySerial(rover=rover,roverDataCollection=roverDataCollection)
    else:
        mongoInsertRover(rover=rover,dataCollection=roverDataCollection)
    
def mongoUpdateRoverBySerial(rover,roverDataCollection):
    roverDataCollection.update_one({'serial': rover.serial}, {'$set': {'battery': rover.battery, 'workingStatus': rover.workingStatus, 'location': {
            'lat': rover.lat, 'lon': rover.lon}}})
    print('ROVER UPDATED')

def mongoInsertRover(rover,roverDataCollection):
    roverDataCollection.insert_one({'serial': rover.serial, 'battery': rover.battery, 'location': {
            'lat': rover.lat, 'lon': rover.lon}, 'workingStatus': False,'roverStatus':"Free"})
    print('ROVER ADDED')

def mongoUpdateDroneStatus(rover,droneDataCollection,status):
    droneDataCollection.update_one({'serial': rover.droneSerial}, {'$set': {'droneStatus': status}})
    rover.droneStatus=status
    print('DRONE STATUS UPDATED')

def mongoUpdateRoverStatus(rover,roverDataCollection,status):
    roverDataCollection.update_one({'serial': rover.serial}, {'$set': {'roverStatus': status}})
    rover.roverStatus=status
    print('DRONE STATUS UPDATED')  

    