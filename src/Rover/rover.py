from pymavlink import mavutil
import time

from ..Ultrasonic import *

class Rover:
    def __init__(self,roverSerial,connection):
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
        self.ul_front_edge = Ultrasonic(21,22)
        self.ul_front_next = Ultrasonic(13,14)
        self.ul_back_edge = Ultrasonic(7,8)
        self.ul_back_next = Ultrasonic(17,18)


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


    def setupAndArm(self):
        self.vehicle.mav.command_long_send(self.vehicle.target_system, self.vehicle.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

        self.vehicle.mav.command_long_encode(
		0, 0,
		mavutil.mavlink.MAV_CMD_DO_SET_REVERSE,
		0,
		1,
		0,
		0,
		0,
		0,0, 0)

    def moveForward(self, speed):
        self.vehicle.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, self.vehicle.target_system,
                        self.vehicle.target_component, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, int(0b110111000111), 0, 0, 0, speed, 0, 0, 0, 0, 0, 0, 0))

    def moveBackward(self, speed):
        self.vehicle.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, self.vehicle.target_system,
                        self.vehicle.target_component, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, int(0b11011100111), 0, 0, 0, -(speed), 0, 0, 0, 0, 0, 0, 0))

    def changeYaw(self, angle):
        self.vehicle.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, self.vehicle.target_system,
                        self.vehicle.target_component, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED , int(0b100111100111), 0, 0, 0, 0, 0, 0, 0, 0, 0, angle, 0))

if __name__== "__main__":
    pass