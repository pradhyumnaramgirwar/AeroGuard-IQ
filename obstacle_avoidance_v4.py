import time
from dronekit import connect, VehicleMode
from pymavlink import mavutil

print("--- AeroGuard-IQ: The Bare-Metal MAVLink Ascent (Patched) ---")

# Connect to the SITL simulator
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=False)

def send_velocity_cmd(vx, vy, vz):
    """
    Phase 5 Logic: Sends raw MAVLink velocity commands to the drone.
    Used for both moving and emergency braking.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0, 0, 0, mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111, 0, 0, 0, vx, vy, vz, 0, 0, 0, 0, 0)
    vehicle.send_mavlink(msg)

def run_mission():
    print("[1] Initializing Autopilot...")
    while vehicle.version is None:
        time.sleep(1)

    print("[2] Muting Hardware Alarms...")
    try:
        vehicle.parameters['ARMING_CHECK'] = 0
        vehicle.parameters['FS_THR_ENABLE'] = 0
    except:
        pass

    print("[3] Waiting for Sensors (Bulletproof Check)...")
    while True:
        # Prevents Python crashes by strictly validating NoneType telemetry
        gps = 0
        if getattr(vehicle, 'gps_0', None) is not None:
            val = getattr(vehicle.gps_0, 'fix_type', None)
            if val is not None:
                gps = val
        
        ekf = False
        if getattr(vehicle, 'ekf_ok', None) is not None:
            ekf = vehicle.ekf_ok
            
        print(f"  GPS: {gps} | EKF: {ekf}")
        if gps >= 3 and ekf:
            break
        time.sleep(2)

    print("[4] Securing Home Location...")
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()
    while not vehicle.home_location:
        time.sleep(1)
    print(" >>> HOME LOCKED.")

    print("[5] Switching to GUIDED Mode...")
    # Bypassing DroneKit's text-translation bug with raw mode 4
    for _ in range(3):
        vehicle._master.set_mode(4)
        time.sleep(1)
    print(" >>> MODE COMMAND SENT.")
    time.sleep(2) 

    print("[6] Bypassing DroneKit: Injecting Raw ARM Command...")
    msg_arm = vehicle.message_factory.command_long_encode(
        0, 0, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 
        1, 0, 0, 0, 0, 0, 0) # 1 = Arm
    vehicle.send_mavlink(msg_arm)
    
    time.sleep(3)
    if vehicle.armed:
        print(" >>> MOTORS ARMED SUCCESSFULLY.")
    else:
        print("  Forcing secondary raw arm packet...")
        vehicle.send_mavlink(msg_arm)
        time.sleep(3)

    print("[7] Bypassing DroneKit: Injecting Raw TAKEOFF Command (10m)...")
    msg_takeoff = vehicle.message_factory.command_long_encode(
        0, 0, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 
        0, 0, 0, 0, 0, 0, 10) # 10 = Target Altitude
    vehicle.send_mavlink(msg_takeoff)
    
    # Phase 4: Monitor Ascent
    while True:
        alt = getattr(vehicle.location.global_relative_frame, 'alt', 0.0) or 0.0
        print(f"  Altitude: {alt:.2f}m")
        if alt >= 9.5:
            print(" >>> TARGET REACHED.")
            break
        time.sleep(1)

    print("\n[8] Phase 5: Active Obstacle Avoidance Loop...")
    # This loop simulates the drone moving North while scanning for objects
    for _ in range(15):
        dist = getattr(vehicle.rangefinder, 'distance', None)
        if dist is not None and dist < 7.0:
            print(f" !!! OBSTACLE AT {dist:.2f}m -> EMERGENCY BRAKING !!!")
            send_velocity_cmd(0, 0, 0) # Stop all movement
        else:
            readout = f"{dist:.2f}m" if dist is not None else "Scanning..."
            print(f"  [Path Clear] Moving North @ 2m/s | Sensor: {readout}")
            send_velocity_cmd(2, 0, 0) # Maintain forward velocity
        time.sleep(1)

    print("\n[9] Landing via Raw Command...")
    vehicle._master.set_mode(9) # Mode 9 = LAND
    while True:
        alt = getattr(vehicle.location.global_relative_frame, 'alt', 0.0) or 0.0
        print(f"  Descending: {alt:.2f}m")
        if alt <= 0.3:
            break
        time.sleep(1)

    print("\n>>> MISSION SUCCESS.")

if __name__ == "__main__":
    try:
        run_mission()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    finally:
        if 'vehicle' in locals():
            vehicle.close()