import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../','.env')
load_dotenv(dotenv_path)

MONGODB_ATLAS_URL = os.getenv('MONGODB_ATLAS_URL')
DATABASE = os.getenv('DATABASE')
DRONE_COLLECTION = os.getenv('DRONE_COLLECTION')
ROVER_COLLECTION = os.getenv('ROVER_COLLECTION')

print('Database: ' + DATABASE)
print('DRONE_COLLECTION: ' + DRONE_COLLECTION)
print('ROVER_COLLECTION: ' + ROVER_COLLECTION)


def getserial():
    cpuserial = "ERROR000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
    return cpuserial