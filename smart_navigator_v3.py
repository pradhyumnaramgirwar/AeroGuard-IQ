import time
import csv
from dronekit import connect, VehicleMode, LocationGlobalRelative

# 1. Connect to AeroGuard-IQ
print("Connecting to AeroGuard-IQ (Phase 3: Final Safety Upgrades)...")
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=False)

def check_safety_and_adjust(writer):
    """The 'Brain' with Heartbeat and Battery Failsafes"""
    
    # --- 1. Heartbeat Watchdog (Connection Safety) ---
    if vehicle.last_heartbeat > 5:
        print(f"!!! LOST CONNECTION: No heartbeat for {vehicle.last_heartbeat:.1f}s !!!")
        vehicle.mode = VehicleMode("LAND")
        return False

    volt = vehicle.battery.voltage
    alt = vehicle.location.global_relative_frame.alt
    
    # --- 2. Battery Watchdog ---
    if volt < 10.5:
        print(f"!!! CRITICAL BATTERY: {volt}V | EMERGENCY RTL !!!")
        vehicle.mode = VehicleMode("RTL")
        return False 

    # --- 3. Altitude 'Nudge' Logic ---
    if alt < 9.0:
        target_pwm = 1380 
        print(f" [Nudge UP] Alt: {alt:.2f}m | PWM: {target_pwm}")
    elif alt > 11.5:
        target_pwm = 1320 
        print(f" [Nudge DOWN] Alt: {alt:.2f}m | PWM: {target_pwm}")
    else:
        target_pwm = 1350 
        
    vehicle.channels.overrides['3'] = target_pwm
    
    # Log telemetry for Phase 3 Analysis
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
            print(f"\n>>> Navigating to Waypoint {i+1}")
            vehicle.simple_goto(wp)
            
            for _ in range(15):
                if not check_safety_and_adjust(writer):
                    return 
                time.sleep(1)

        print("\n--- Phase 5: Verified Landing Sequence ---")
        vehicle.channels.overrides = {}
        vehicle.mode = VehicleMode("LAND")

        # Stay connected until touchdown
        while vehicle.location.global_relative_frame.alt > 0.3:
            print(f" Final Descent... Alt: {vehicle.location.global_relative_frame.alt:.2f}m")
            time.sleep(1)

        print(">>> Touchdown Confirmed. Mission Success.")

try:
    run_mission()
finally:
    print("Closing Connection.")
    vehicle.close()