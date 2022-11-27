import pymongo

def mongoConnect(mongoUrl,database,collection):
    mc = pymongo.MongoClient(mongoUrl)
    mydb = mc[database]
    dataCollection = mydb[collection]
    return dataCollection


def mongoConnectRoverBySerial(rover,dataCollection):
    if dataCollection.find_one({'serial': rover.serial}):
        mongoUpdateRoverBySerial(rover=rover,dataCollection=dataCollection)
    else:
        mongoInsertRover(rover=rover,dataCollection=dataCollection)
    
def mongoUpdateRoverBySerial(rover,dataCollection):
    dataCollection.update_one({'serial': rover.serial}, {'$set': {'battery': rover.battery, 'workingStatus': rover.workingStatus, 'location': {
            'lat': rover.lat, 'lon': rover.lon}}})
    print('ROVER UPDATED')

def mongoInsertRover(rover,dataCollection):
    dataCollection.insert_one({'serial': rover.serial, 'battery': rover.battery, 'location': {
            'lat': rover.lat, 'lon': rover.lon}, 'workingStatus': False})
    print('ROVER ADDED')