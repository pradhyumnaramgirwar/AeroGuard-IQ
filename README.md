# 🚁 AeroGuard-IQ: Autonomous Drone Navigation System
**Master's Project (EEIT) - Otto von Guericke University Magdeburg**
**Developer:** Pradhyumna Avinash Ramgirwar

AeroGuard-IQ is an autonomous flight control system built using Python and DroneKit-SITL. The project focuses on solving altitude stability and implementing self-aware logic for UAVs in a simulated environment (ArduCopter V3.3).

---

## 📈 Project Roadmap & Evolution

### **Phase 1: Stabilization & High-Altitude Achievement**
* **Challenge:** Overcoming initial EKF/GPS altitude drops ("Death Dives").
* **Strategy:** Implemented a **1450 PWM** "Constant Pressure" climb logic.
* **Result:** Successfully completed a 4-waypoint square reaching a peak altitude of **111.79 meters**.
* **Data:** `Phase1_HighAlt_111m.csv`

### **Phase 2: Precision Control & System Identification**
* **Challenge:** Moving from aggressive climbing to a controlled 10m hover.
* **Strategy:** Performed throttle-ramp testing to identify the equilibrium point ($Thrust \approx Weight$).
* **Result:** Identified **1350 PWM** as the "Magic Number" for stable flight. Restricted altitude drift to a damped range of 7m–17m.
* **Data:** `Phase2_Precision_1350PWM_Final.csv`

### **Phase 3: Adaptive Autonomy & Smart Failsafes**
* **Challenge:** Protecting the drone from environmental drift and hardware failure.
* **Strategy:** Implemented **Closed-Loop Feedback** logic (The "Nudge" System).
* **Intelligence:**
    * **Altitude Guard:** Automatically triggers **1380 PWM** if altitude < 9.0m.
    * **Battery Watchdog:** Triggers Emergency **Return-to-Launch (RTL)** if voltage < 10.5V.
* **Result:** Maintained a safe flight envelope (8.7m–15.6m) without manual intervention.
* **Data:** `Phase3_Smart_Log.csv`

---

## 📂 Repository Structure
* `/scripts`: Contains `waypoint_mission.py` (Phase 1/2) and `smart_navigator_v3.py` (Phase 3).
* `/logs`: Comprehensive telemetry data for all flight phases.
* `requirements.txt`: Python dependencies (DroneKit, SITL).

## 🛠️ Technical Stack
* **Language:** Python 3.9
* **Protocol:** MAVLink
* **Simulation:** DroneKit-SITL (Copter-3.3)
* **Concepts:** Proportional Control, System Identification, Autonomous Navigation.

---
*Next Milestone: Phase 4 - Dynamic Mapping and Obstacle Avoidance.*
