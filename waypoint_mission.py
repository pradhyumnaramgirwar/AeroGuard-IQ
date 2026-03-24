import time
from dronekit import connect, VehicleMode, LocationGlobalRelative

# 1. Connect
print("Connecting to AeroGuard-IQ...")
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=False)

def run_mission():
    print("--- Phase 1: Heavy Stabilization (60s) ---")
    # Waiting for the virtual sensors in Magdeburg SITL to settle
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
        print(f" Climbing... Altitude: {vehicle.location.global_relative_frame.alt:.2f}m")
        time.sleep(1)

    print("--- Phase 4: Constant Pressure Navigation ---")
    # Instead of dropping to 0, we hold 1450 to keep the motors spinning
    print(" Reducing to Base Throttle (1450) to prevent drop...")
    vehicle.channels.overrides['3'] = 1450
    time.sleep(2)
    
    # Check if we are holding height
    current_alt = vehicle.location.global_relative_frame.alt
    if current_alt > 7:
        print(f" Stability Confirmed at {current_alt:.2f}m. Moving 10m North...")
        # Move approx 10m North
        target = LocationGlobalRelative(vehicle.location.global_frame.lat + 0.0001, 
                                       vehicle.location.global_frame.lon, 10)
        vehicle.simple_goto(target)
        
        # Monitor for 15 seconds while maintaining 1450 throttle
        for i in range(15):
            print(f" Navigating... Altitude: {vehicle.location.global_relative_frame.alt:.2f}m")
            time.sleep(1)
            
        # Release all overrides before landing
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