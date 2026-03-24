# AeroGuard-IQ
Autonomous Drone Navigation using Python and DroneKit.

## Latest Achievement
- [x] **Stability Handshake:** Successfully implemented a 1450-throttle "Constant Pressure" logic to prevent EKF/GPS altitude drops.
- [x] **Mission Success:** Reached a peak altitude of **47.10 meters** and navigated 10m North autonomously.

## Project Files
* `waypoint_mission.py`: Main autonomous flight logic.
* `flight_log_success_47m.csv`: Telemetry data showing the successful 47m climb.

## How to Run
1. Start SITL: `py -3.9 -m dronekit_sitl copter-3.3`
2. Run Script: `py -3.9 waypoint_mission.py`
