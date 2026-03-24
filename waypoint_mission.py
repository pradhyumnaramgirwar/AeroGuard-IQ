import time
import csv
from dronekit import connect, VehicleMode, LocationGlobalRelative

# 1. Connect to the AeroGuard-IQ SITL
print("Connecting to AeroGuard-IQ...")
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=False)

def run_mission():
    # Use 'w' mode to overwrite old data and start a fresh log
    with open('flight_log.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # Write the Header Row
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
        
        # Climb until 10m
        while vehicle.location.global_relative_frame.alt < 10:
            alt = vehicle.location.global_relative_frame.alt
            print(f" Climbing... Altitude: {alt:.2f}m")
            # Log the data during climb
            writer.writerow([time.time(), vehicle.battery.voltage, alt, 
                             vehicle.location.global_frame.lat, vehicle.location.global_frame.lon])
            time.sleep(1)

        print("--- Phase 4: Constant Pressure Navigation ---")
        # 1450 provides the lift needed for the 47m climb achievement
        print(" Reducing to Base Throttle (1450) to prevent drop...")
        vehicle.channels.overrides['3'] = 1450
        time.sleep(2)
        
        current_alt = vehicle.location.global_relative_frame.alt
        if current_alt > 7:
            print(f" Stability Confirmed at {current_alt:.2f}m. Moving 10m North...")
            target = LocationGlobalRelative(vehicle.location.global_frame.lat + 0.0001, 
                                           vehicle.location.global_frame.lon, 10)
            vehicle.simple_goto(target)
            
            for i in range(15):
                alt = vehicle.location.global_relative_frame.alt
                print(f" Navigating... Altitude: {alt:.2f}m")
                # Log the data during navigation
                writer.writerow([time.time(), vehicle.battery.voltage, alt, 
                                 vehicle.location.global_frame.lat, vehicle.location.global_frame.lon])
                time.sleep(1)
                
            vehicle.channels.overrides = {}
        else:
            print(" Altitude drop detected! Emergency Landing.")

        print("--- Phase 5: Mission Success & Land ---")
        vehicle.mode = VehicleMode("RTL")

try:
    run_mission()
finally:
    print("Closing Connection.")
    vehicle.close()