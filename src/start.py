import time

from .Rover import *
import src.Mongo as Mongo

def initRoverOnMongo(rover,dataCollection):
    Mongo.mongoConnectRoverBySerial(rover=rover,dataCollection=dataCollection)

def cleanArea():
    print('cleaning')

def mainStart(serial=None, connection=None,dataCollection=None):
    if serial != None:
        print(serial)
        rover = Rover(roverSerial=serial,connection=connection)
        print(rover)
        initRoverOnMongo(rover=rover,dataCollection=dataCollection)
        cleanArea()

if __name__ == '__main__':
    pass
else:
    mainStart()