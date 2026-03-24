# AeroGuard-IQ
Autonomous Drone Control using DroneKit and ArduPilot SITL.

## Project Goal
This project demonstrates a forced-takeoff sequence to 20 meters, bypassing common EKF and GPS safety locks in a simulated environment (SITL).

## How to Run
1. Start the SITL: `py -3.9 -m dronekit_sitl copter-3.3`
2. Run the script: `py -3.9 hello_drone.py`

## Current Status
- [x] Initial Connection Established
- [x] Forced Takeoff to 20m Successful
- [ ] Autonomous Waypoint Navigation (Coming Soon)
