import time
import csv
from dronekit import connect, VehicleMode, LocationGlobalRelative

# 1. Connect to AeroGuard-IQ
print("Connecting to AeroGuard-IQ...")
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=False)

def run_mission():
    # 'w' mode ensures a fresh log for Phase 2 data analysis
    with open('hover_tune_log.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Voltage', 'Altitude', 'PWM_Value'])

        print("--- Phase 1: Heavy Stabilization (60s) ---")
        time.sleep(60) 

        print("--- Phase 2: Safety Bypass & Forced Arm ---")
        vehicle.parameters['ARMING_CHECK'] = 0 
        vehicle.parameters['FS_EKF_THRESH'] = 1.0
        vehicle.mode = VehicleMode("GUIDED")
        
        while not vehicle.armed:
            print(" Forcing Arm...")
            vehicle.armed = True
            time.sleep(2)

        print("--- Phase 3: Initial Climb to 10m ---")
        vehicle.channels.overrides['3'] = 1500
        while vehicle.location.global_relative_frame.alt < 10:
            alt = vehicle.location.global_relative_frame.alt
            print(f" Initial Climb: {alt:.2f}m")
            time.sleep(1)

        print("--- Phase 4: The Precision Tuning Loop ---")
        # We test 4 different power levels to find the 'Magic Number'
        test_pwm_values = [1450, 1420, 1400, 1380]
        
        for pwm in test_pwm_values:
            print(f"\n>>> TESTING THROTTLE: {pwm} PWM")
            vehicle.channels.overrides['3'] = pwm
            
            # Observe for 10 seconds at this specific power
            for i in range(10):
                alt = vehicle.location.global_relative_frame.alt
                print(f" [Test {i+1}/10] PWM: {pwm} | Altitude: {alt:.2f}m")
                writer.writerow([time.time(), vehicle.battery.voltage, alt, pwm])
                time.sleep(1)

        print("\n--- Phase 5: Mission Success & Land ---")
        vehicle.channels.overrides = {} # Release overrides for clean landing
        vehicle.mode = VehicleMode("RTL")

try:
    run_mission()
finally:
    print("Closing Connection.")
    vehicle.close()
