# AeroGuard-IQ: Autonomous Drone Navigation
Master's Project (EEIT) - Otto von Guericke University Magdeburg

## 🚀 Final Project Achievement: 100% Complete
- [x] **Stability Handshake:** Successfully implemented a 1450-throttle "Constant Pressure" logic to prevent ArduCopter 3.3 EKF/GPS altitude drops.
- [x] **High-Altitude Square Mission:** Reached a peak altitude of **111.79 meters**.
- [x] **Geometric Navigation:** Completed an autonomous 4-waypoint square pattern (North -> East -> South -> West) with real-time telemetry logging.

## 📁 Project Structure
* `waypoint_mission.py`: Final mission script with multi-waypoint logic and 'Write' mode telemetry.
* `flight_log_square_mission_111m.csv`: Complete telemetry log from the successful 111m square flight.
* `requirements.txt`: Python dependencies for the project.

## 🛠️ Technical Implementation
The system uses **DroneKit-SITL** and **Python 3.9**. It bypasses standard arming checks to simulate emergency autonomous maneuvers and uses a constant throttle override to maintain lift during GPS coordinate transitions.
