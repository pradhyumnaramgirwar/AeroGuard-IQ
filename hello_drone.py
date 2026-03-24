import time
import csv
from dronekit import connect, VehicleMode

# 1. Connect
print("Connecting to AeroGuard-IQ...")
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=False)

def log_telemetry(file_writer):
    """Function to grab current data and write to CSV"""
    row = [
        time.strftime("%H:%M:%S"),
        vehicle.battery.voltage,
        vehicle.gps_0.satellites_visible,
        vehicle.groundspeed,
        vehicle.location.global_relative_frame.alt
    ]
    file_writer.writerow(row)

def mission_with_logging():
    # Setup CSV File
    with open('flight_log.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Voltage', 'Sats', 'Speed', 'Altitude'])

        print("--- Phase 1: Stabilization ---")
        time.sleep(20) 
        
        print("--- Phase 2: Safety Bypasses ---")
        vehicle.parameters['ARMING_CHECK'] = 0 
        vehicle.parameters['FS_EKF_THRESH'] = 1.0
        vehicle.parameters['FS_EKF_ACTION'] = 0 
        
        print("--- Phase 3: Forcing Motors ---")
        vehicle.mode = VehicleMode("STABILIZE")
        while not vehicle.armed:
            vehicle.armed = True
            time.sleep(2)

        print("--- Phase 4: Takeoff & Data Logging ---")
        vehicle.channels.overrides['3'] = 1500
        
        # Log data for 15 seconds during flight
        for i in range(15):
            alt = vehicle.location.global_relative_frame.alt
            print(f" Altitude: {alt if alt else 0:.2f}m | Battery: {vehicle.battery.voltage}V")
            
            # SAVE DATA TO FILE
            log_telemetry(writer)
            time.sleep(1)

        print("--- Phase 5: Landing ---")
        vehicle.channels.overrides = {}
        vehicle.mode = VehicleMode("LAND")

try:
    mission_with_logging()
finally:
    vehicle.close()
    print("Mission Complete. Check 'flight_log.csv' for data!")
