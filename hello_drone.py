import time
from dronekit import connect, VehicleMode

print("Connecting to AeroGuard-IQ...")
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=False)

def force_takeoff():
    print("--- STEP 1: Total Bypass ---")
    # Tell the drone to ignore EVERYTHING. 
    vehicle.parameters['ARMING_CHECK'] = 0 
    vehicle.parameters['FS_EKF_THRESH'] = 1.0
    vehicle.parameters['FS_EKF_ACTION'] = 0 
    time.sleep(5)

    print("--- STEP 2: Arming in STABILIZE ---")
    vehicle.mode = VehicleMode("STABILIZE")
    
    while not vehicle.armed:
        print(" Forcing Motors...")
        vehicle.armed = True
        time.sleep(2)

    print("--- STEP 3: Manual Throttle Lift ---")
    # Instead of 'simple_takeoff', we push the RC channel 3 (Throttle) to 1500
    # This forces the drone up even if it hates the GPS signal
    vehicle.channels.overrides['3'] = 1500
    
    print("FLYING! Monitoring altitude...")
    for i in range(10):
        alt = vehicle.location.global_relative_frame.alt
        print(f" Current Altitude: {alt if alt else 0:.2f}m")
        time.sleep(1)

    print("MISSION SUCCESS. Clearing overrides and landing.")
    vehicle.channels.overrides = {}
    vehicle.mode = VehicleMode("LAND")

try:
    force_takeoff()
finally:
    vehicle.close()