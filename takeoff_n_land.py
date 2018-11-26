# -*- coding: utf-8 -*-
"""
Author:     Tyler Mason
Class:      AAE 45000 - Spacecraft Senior Design
Purpose:    Autonomous takeoff and land, not implementing the LIDAR yet due to 
            version issues with the LIDAR and the board. Need to upgrade board. 
            This script should be close to working when a new board is utilized.
"""
#Imports required for autonomous takeoff
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import argparse  

#connect to the default drone IP - may need to change in future iterations
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550') #default drone IP
args = parser.parse_args()

# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % args.connect
vehicle = connect(args.connect, baud=57600, wait_ready=True)

# Function to arm and then takeoff to a user specified altitude
def arm_rotocraft():
    
  while not vehicle.is_armable:
    print(" Waiting for vehicle to initialise...")
    time.sleep(1)
        
  print("Arming motors")
  # Copter should arm in GUIDED mode
  vehicle.mode    = VehicleMode("GUIDED")
  vehicle.armed   = True

  while not vehicle.armed:
    print " Waiting for arming..."
    time.sleep(1)   
    
def takeoff_scheme(h_des):

  print "Taking off!"
  vehicle.simple_takeoff(h_des) # Take off to target altitude

  # Check that vehicle has reached takeoff altitude
  while True:
    print " Altitude: ", vehicle.location.global_relative_frame.alt #this should grab data from the LIDAR       
    if vehicle.location.global_relative_frame.alt>=h_des*0.99: #stop just before 
      print "At target altitude"
      break
    time.sleep(1)

# Initialize the quad
arm_rotocraft()
#takeoff
takeoff_scheme(10) #takeoff to 10 meters
print("Take off complete")
# Hover for 5 seconds
time.sleep(5)

print("Initialize landing sequence")
vehicle.mode = VehicleMode("LAND")

# Close vehicle object
vehicle.close()