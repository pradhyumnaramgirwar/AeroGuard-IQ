# AeroGuard-IQ
Autonomous Drone Control using DroneKit and ArduPilot SITL.

## Project Goal
This project demonstrates a robust autonomous flight sequence in a simulated environment (SITL), focusing on bypassing safety locks and maintaining stability during mode transitions.

## Key Technical Achievements
* **The "Stability Handshake":** Developed a hybrid control logic (Manual Throttle + Guided Mode) to prevent altitude drops during autonomous handovers.
* **Telemetry Data:** Integrated real-time logging of Altitude, Battery, and GPS to CSV.

## How to Run
1. Start the SITL: `py -3.9 -m dronekit_sitl copter-3.3`
2. Run the Main Mission: `py -3.9 waypoint_mission.py`

## Current Status
- [x] Initial Connection Established
- [x] Forced Takeoff to 20m Successful
- [x] Autonomous Waypoint Navigation (Reached 46m altitude)
- [ ] Precision Altitude Tuning (Target: 10m Stable Hover)
