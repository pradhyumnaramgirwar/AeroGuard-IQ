# 🚁 AeroGuard-IQ: Autonomous Drone Navigation System
**Master's Project (EEIT) - Otto von Guericke University Magdeburg**
**Developer:** Pradhyumna Avinash Ramgirwar

AeroGuard-IQ is an autonomous flight control system built using Python and DroneKit-SITL. The project focuses on solving altitude stability and implementing self-aware logic for UAVs in a simulated environment (ArduCopter V3.3).

---

## 📈 Project Roadmap & Evolution

### **Phase 1: Stabilization & High-Altitude**
* **Challenge:** Overcoming initial EKF/GPS altitude drops ("Death Dives").
* **Strategy:** Implemented a **1450 PWM** "Constant Pressure" climb logic.
* **Data:** `flight_log.csv`

### **Phase 2: Precision Control & System Identification**
* **Challenge:** Identifying the exact equilibrium point ($Thrust \approx Weight$).
* **Strategy:** Performed throttle-ramp testing to find the neutral buoyancy point.
* **Result:** Identified **1350 PWM** as the equilibrium constant.
* **Data:** `Phase2_Precision_1350PWM_Final.csv`

### **Phase 3: Adaptive Autonomy & Smart Failsafes (Current)**
* **Challenge:** Protecting the drone from environmental drift and connection loss.
* **Intelligence & Safety Limits:**
    * **Altitude Guard (Closed-Loop):** Automatically triggers **1380 PWM** if altitude < 9.0m. This 9m threshold was chosen to provide a 1-second reaction buffer before ground contact.
    * **Connection Watchdog:** Monitored via `last_heartbeat`. Triggers **LAND** mode if link is lost for > 5s.
    * **Battery Watchdog:** Emergency **RTL** if voltage < 10.5V.
* **Data:** `Phase3_Smart_Log.csv`

### **📊 Phase 3 Results Table**

| Metric | Safety Threshold | Phase 3 Peak Result | Status |
| :--- | :--- | :--- | :--- |
| **Altitude Floor** | > 8.5m | **8.71m (Corrected)** | ✅ PASS |
| **Altitude Ceiling** | < 16.0m | **15.64m (Corrected)** | ✅ PASS |
| **Battery Level** | > 10.5V | **11.2V (Safe)** | ✅ PASS |
| **Landing Verify** | < 0.3m | **0.28m (Touchdown)** | ✅ PASS |

---

## 📂 Repository Structure
* `/scripts`: `waypoint_mission.py`, `smart_navigator_v3.py`.
* `/logs`: Telemetry data for all flight phases (CSVs).
* `requirements.txt`: Python dependencies.
* `LICENSE`: MIT License.

## 🛠️ Technical Stack
* **Language:** Python 3.9 | **Protocol:** MAVLink | **Simulation:** DroneKit-SITL (Copter-3.3)

---

## 🚀 Future Work: Phase 4
The next evolution of AeroGuard-IQ will focus on **Environmental Awareness**:
* **Obstacle Avoidance:** Integrating simulated distance sensors to deviate from the path when objects are detected.
* **Dynamic Mapping:** Real-time plotting of flight paths using Matplotlib for visual mission oversight.
