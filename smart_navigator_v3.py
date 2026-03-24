import time
import csv
from dronekit import connect, VehicleMode, LocationGlobalRelative

# 1. Connect to AeroGuard-IQ
print("Connecting to AeroGuard-IQ (Phase 3: Smart Autonomy)...")
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=False)

def check_safety_and_adjust(writer):
    """The 'Brain' of Phase 3: Monitors Battery and Altitude"""
    volt = vehicle.battery.voltage
    alt = vehicle.location.global_relative_frame.alt
    current_pwm = vehicle.channels.overrides.get('3', 1350)
    
    # --- 1. Battery Watchdog ---
    if volt < 10.5:
        print(f"!!! CRITICAL BATTERY: {volt}V | EMERGENCY RTL !!!")
        vehicle.mode = VehicleMode("RTL")
        return False # This will break the mission loop

    # --- 2. Altitude 'Nudge' Logic (Basic Proportional Control) ---
    # We use your 1350 'Magic Number' as the base
    if alt < 9.0:
        target_pwm = 1380 # Give it a little boost
        print(f" [Nudge UP] Alt: {alt:.2f}m | New PWM: {target_pwm}")
    elif alt > 11.5:
        target_pwm = 1320 # Let it sink a bit
        print(f" [Nudge DOWN] Alt: {alt:.2f}m | New PWM: {target_pwm}")
    else:
        target_pwm = 1350 # Stay at Equilibrium
        
    vehicle.channels.overrides['3'] = target_pwm
    
    # Log everything for Phase 3 Analysis
    writer.writerow([time.time(), volt, alt, target_pwm])
    return True

def run_mission():
    filename = 'Phase3_Smart_Log.csv'
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Voltage', 'Altitude', 'PWM_Value'])

        print("--- Phase 1: Stabilization (60s) ---")
        time.sleep(60) 

        print("--- Phase 2: Safety Bypass & Arm ---")
        vehicle.parameters['ARMING_CHECK'] = 0 
        vehicle.parameters['FS_EKF_THRESH'] = 1.0
        vehicle.mode = VehicleMode("GUIDED")
        
        while not vehicle.armed:
            vehicle.armed = True
            time.sleep(2)

        print("--- Phase 3: Initial Climb to 10m ---")
        vehicle.channels.overrides['3'] = 1500
        while vehicle.location.global_relative_frame.alt < 10:
            time.sleep(1)

        print("--- Phase 4: Smart Square Mission ---")
        start_lat = vehicle.location.global_frame.lat
        start_lon = vehicle.location.global_frame.lon
        
        waypoints = [
            LocationGlobalRelative(start_lat + 0.0001, start_lon, 10),
            LocationGlobalRelative(start_lat + 0.0001, start_lon + 0.0001, 10),
            LocationGlobalRelative(start_lat, start_lon + 0.0001, 10),
            LocationGlobalRelative(start_lat, start_lon, 10)
        ]

        for i, wp in enumerate(waypoints):
            print(f"\n>>> Moving to Waypoint {i+1}")
            vehicle.simple_goto(wp)
            
            # Watch the drone for 15 seconds during each leg
            for _ in range(15):
                # Run the 'Brain' check
                continue_mission = check_safety_and_adjust(writer)
                if not continue_mission:
                    return # Exit mission if battery is low
                time.sleep(1)

        print("\n--- Phase 5: Mission Success & Land ---")
        vehicle.channels.overrides = {}
        vehicle.mode = VehicleMode("RTL")

try:
    run_mission()
finally:
    print("Closing Connection.")
    vehicle.close()