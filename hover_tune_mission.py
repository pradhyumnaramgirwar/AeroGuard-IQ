import time
import csv
from dronekit import connect, VehicleMode, LocationGlobalRelative

# 1. Connect to AeroGuard-IQ
print("Connecting to AeroGuard-IQ...")
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=False)

def run_mission():
    # This specific filename ensures we don't look at old Phase 1 data
    output_file = 'Phase2_Precision_1350PWM_Final.csv'
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Voltage', 'Altitude', 'Lat', 'Lon', 'PWM_Value'])

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
        target_pwm = 1350
        vehicle.channels.overrides['3'] = target_pwm 
        
        start_lat = vehicle.location.global_frame.lat
        start_lon = vehicle.location.global_frame.lon
        
        waypoints = [
            LocationGlobalRelative(start_lat + 0.0001, start_lon, 10),
            LocationGlobalRelative(start_lat + 0.0001, start_lon + 0.0001, 10),
            LocationGlobalRelative(start_lat, start_lon + 0.0001, 10),
            LocationGlobalRelative(start_lat, start_lon, 10)
        ]

        for i, wp in enumerate(waypoints):
            print(f" >>> Moving to Waypoint {i+1}...")
            vehicle.simple_goto(wp)
            for _ in range(12):
                alt = vehicle.location.global_relative_frame.alt
                print(f" WP {i+1} | PWM: {target_pwm} | Alt: {alt:.2f}m")
                writer.writerow([time.time(), vehicle.battery.voltage, alt, 
                                 vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, target_pwm])
                time.sleep(1)

        print(f"--- Phase 5: Success! Data saved to {output_file} ---")
        vehicle.channels.overrides = {}
        vehicle.mode = VehicleMode("RTL")

try:
    run_mission()
finally:
    print("Closing Connection.")
    vehicle.close()
