import time
import csv
from dronekit import connect, VehicleMode, LocationGlobalRelative

# 1. Connect to AeroGuard-IQ
print("Connecting to AeroGuard-IQ...")
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=False)

def run_mission():
    with open('precision_square_log.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Voltage', 'Altitude', 'Lat', 'Lon'])

        print("--- Phase 1: Stabilization (60s) ---")
        time.sleep(60) 

        print("--- Phase 2: Safety Bypass & Arm ---")
        vehicle.parameters['ARMING_CHECK'] = 0 
        vehicle.parameters['FS_EKF_THRESH'] = 1.0
        vehicle.mode = VehicleMode("GUIDED")
        
        while not vehicle.armed:
            print(" Forcing Arm...")
            vehicle.armed = True
            time.sleep(2)

        print("--- Phase 3: Climb to 10m ---")
        vehicle.channels.overrides['3'] = 1500
        while vehicle.location.global_relative_frame.alt < 10:
            print(f" Climbing... Altitude: {vehicle.location.global_relative_frame.alt:.2f}m")
            time.sleep(1)

        print("--- Phase 4: Precision Square (1350 PWM) ---")
        # Applying the Phase 2 'Magic Number' for stable altitude
        vehicle.channels.overrides['3'] = 1350 
        
        start_lat = vehicle.location.global_frame.lat
        start_lon = vehicle.location.global_frame.lon
        
        waypoints = [
            LocationGlobalRelative(start_lat + 0.0001, start_lon, 10),            # North
            LocationGlobalRelative(start_lat + 0.0001, start_lon + 0.0001, 10),   # East
            LocationGlobalRelative(start_lat, start_lon + 0.0001, 10),            # South
            LocationGlobalRelative(start_lat, start_lon, 10)                     # Home
        ]

        for i, wp in enumerate(waypoints):
            print(f" >>> Moving to Waypoint {i+1}...")
            vehicle.simple_goto(wp)
            for _ in range(12):
                alt = vehicle.location.global_relative_frame.alt
                print(f" Navigating WP {i+1}... Altitude: {alt:.2f}m")
                writer.writerow([time.time(), vehicle.battery.voltage, alt, 
                                 vehicle.location.global_frame.lat, vehicle.location.global_frame.lon])
                time.sleep(1)

        print("--- Phase 5: Mission Success & Land ---")
        vehicle.channels.overrides = {}
        vehicle.mode = VehicleMode("RTL")

try:
    run_mission()
finally:
    print("Closing Connection.")
    vehicle.close()