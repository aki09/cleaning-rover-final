from pymavlink import mavutil
import time

class Rover:
    def __init__(self,roverSerial,connection):
        print('start')
        vehicle = mavutil.mavlink_connection(connection)
        vehicle.wait_heartbeat()
        print("Heartbeat from system (system %u component %u)" % (vehicle.target_system, vehicle.target_component))

        _ = vehicle.messages.keys() #All parameters that can be fetched

        pos = vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        system = vehicle.recv_match(type='SYS_STATUS', blocking=True)

        self.serial=roverSerial
        self.lat=pos.lat * 10e-8
        self.lon=pos.lon * 10e-8
        self.battery=system.battery_remaining
        self.vehicle=vehicle
        self.workingStatus=False


    def changeVehicleMode(self,mode):
        print("Changing vehicle mode to",mode)
        # Get mode ID
        mode_id = self.vehicle.mode_mapping()[mode]
        # Set new mode

        self.vehicle.mav.set_mode_send(
            self.vehicle.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode_id)
        msg = self.vehicle.recv_match(type='COMMAND_ACK', blocking=True)
        print(msg)