# AeroGuard-IQ: Autonomous Drone Navigation System
**Master's Project (EEIT) - Otto von Guericke University Magdeburg**

## 🚀 Project Achievement: 100% Complete
This project implements an autonomous geometric flight mission using Python and DroneKit-SITL. The primary engineering challenge was overcoming a "Death Dive" altitude drop in the ArduCopter 3.3 firmware by implementing a custom stability handshake.

### **Phase 1: Basic Stability & Logic**
- [x] **Stability Handshake:** Successfully implemented a 1450-throttle "Constant Pressure" logic to bypass EKF/GPS altitude drops.
- [x] **High-Altitude Mission:** Reached a peak altitude of **111.79 meters**.
- [x] **Geometric Navigation:** Completed an autonomous 4-waypoint square pattern (North -> East -> South -> West) with real-time telemetry logging.

### **Phase 2: Precision Control (1350 PWM)**
- [x] **System Identification:** Conducted throttle-ramp tests to find the 1350 PWM equilibrium.
- [x] **Damped Altitude Control:** Successfully restricted altitude drift to a stable range (7m - 17m) during a square mission.

## 📁 Project Structure
* `waypoint_mission.py`: Final mission script with multi-waypoint logic and 'Write' mode telemetry.
* `flight_log_square_mission_111m.csv`: Complete telemetry log from the successful 111m square flight.
* `hello_drone.py`: Initial connection and heartbeat testing script.
* `requirements.txt`: Python dependencies (DroneKit & SITL).

## 🛠️ Technical Specifications
- **Language:** Python 3.9
- **Simulator:** DroneKit-SITL (ArduCopter V3.3)
- **Control Strategy:** Forced Guided Mode with Channel Override stabilization.
- **Data Persistence:** Real-time CSV logging of Voltage, Altitude, and GPS Coordinates.

## 🏁 How to Run
1. **Start the Simulator:**
   `py -3.9 -m dronekit_sitl copter-3.3`
2. **Execute the Mission:**
   `py -3.9 waypoint_mission.py`
3. **Review Telemetry:**
   Open `flight_log.csv` to see the flight path data.

---
*Developed by Pradhyumna Avinash Ramgirwar (2026)*
