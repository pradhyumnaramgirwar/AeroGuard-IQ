import time
import csv
from dronekit import connect, VehicleMode, LocationGlobalRelative

# 1. Connect to the AeroGuard-IQ SITL
print("Connecting to AeroGuard-IQ...")
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=False)

def run_mission():
    # 'w' mode ensures a fresh, clean log for every flight
    with open('flight_log.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Voltage', 'Altitude', 'Lat', 'Lon'])

        print("--- Phase 1: Heavy Stabilization (60s) ---")
        time.sleep(60) 

        print("--- Phase 2: Total Safety Bypass ---")
        vehicle.parameters['ARMING_CHECK'] = 0 
        vehicle.parameters['FS_EKF_THRESH'] = 1.0
        vehicle.parameters['FS_EKF_ACTION'] = 0 
        
        print("--- Phase 3: Forced Takeoff ---")
        vehicle.mode = VehicleMode("GUIDED")
        while not vehicle.armed:
            print(" Forcing Arm...")
            vehicle.armed = True
            time.sleep(2)

        print("Kicking Throttle to 50% (1500)...")
        vehicle.channels.overrides['3'] = 1500
        
        # Climb to 10m
        while vehicle.location.global_relative_frame.alt < 10:
            alt = vehicle.location.global_relative_frame.alt
            print(f" Climbing... Altitude: {alt:.2f}m")
            writer.writerow([time.time(), vehicle.battery.voltage, alt, 
                             vehicle.location.global_frame.lat, vehicle.location.global_frame.lon])
            time.sleep(1)

        print("--- Phase 4: Multi-Waypoint Square Mission ---")
        vehicle.channels.overrides['3'] = 1450 # Maintain Constant Lift
        
        # Capture starting position
        start_lat = vehicle.location.global_frame.lat
        start_lon = vehicle.location.global_frame.lon
        
        # Define 4 Corners (North, East, South, West back to start)
        # 0.0001 degrees is roughly 10-11 meters
        waypoints = [
            LocationGlobalRelative(start_lat + 0.0001, start_lon, 10),            # Point 1: North
            LocationGlobalRelative(start_lat + 0.0001, start_lon + 0.0001, 10),   # Point 2: East
            LocationGlobalRelative(start_lat, start_lon + 0.0001, 10),            # Point 3: South
            LocationGlobalRelative(start_lat, start_lon, 10)                     # Point 4: Back Home
        ]

        for i, wp in enumerate(waypoints):
            print(f" >>> Moving to Waypoint {i+1}...")
            vehicle.simple_goto(wp)
            # Give the drone 12 seconds to reach each corner while logging
            for _ in range(12):
                alt = vehicle.location.global_relative_frame.alt
                print(f" Navigating WP {i+1}... Altitude: {alt:.2f}m")
                writer.writerow([time.time(), vehicle.battery.voltage, alt, 
                                 vehicle.location.global_frame.lat, vehicle.location.global_frame.lon])
                time.sleep(1)

        print("--- Phase 5: Mission Success & Land ---")
        vehicle.mode = VehicleMode("RTL")

try:
    run_mission()
finally:
    print("Closing Connection.")
    vehicle.close()