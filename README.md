# AeroGuard-IQ: Autonomous Drone Navigation System
**Master's Project (EEIT) - Otto von Guericke University Magdeburg**

## 🚀 Project Status: Phase 3 Complete (100%)
This project implements an autonomous geometric flight mission using Python and DroneKit-SITL. The primary challenge was overcoming the "Death Dive" altitude drop in ArduCopter 3.3 by implementing a custom stability handshake and throttle tuning.

---

## 📂 Phase 1: Stability & High-Altitude (Achievement)
- **Problem:** Initial flights suffered from EKF/GPS altitude drops, leading to crashes.
- **Solution:** Implemented a 1450 PWM "Constant Pressure" logic.
- **Result:** Successfully reached a peak altitude of **111.79 meters** during a 4-waypoint square mission.
- **Data:** `Phase1_HighAlt_111m.csv`

## 🎯 Phase 2: Precision Control & Tuning (Achievement)
- **Objective:** Move from "Climbing" to "Precision Hover" at 10m.
- **System Identification:** Conducted throttle-ramp tests (1450 -> 1420 -> 1400 -> 1380) to find the equilibrium point.
- **Result:** Identified **1350 PWM** as the "Magic Number" for stable flight ($Thrust \approx Weight$).
- **Success:** Completed a 4-waypoint square with altitude restricted to a damped range (7m - 17m).
- **Data:** `Phase2_Precision_1350PWM_Final.csv`

## 🧠 Phase 3: Adaptive Autonomy & Failsafes (Completed)
In this phase, the system transitioned from "Static Overrides" to "Reactive Logic," allowing the drone to monitor its own state and correct flight errors in real-time.

### **Key Technical Wins:**
- **Closed-Loop Feedback:** Implemented a "Nudge" logic that monitors altitude every 1 second.
- **Altitude Floor:** Successfully prevented the Phase 2 "sink" by triggering a **1380 PWM** boost whenever altitude dropped below **9.0m**.
- **Battery Watchdog:** Integrated a background failsafe to trigger **Return-to-Launch (RTL)** if voltage drops below **10.5V**.

### **Flight Performance (Adaptive Logic):**
* **Minimum Altitude:** 8.73m (Successfully caught and corrected by the script).
* **Maximum Altitude:** 15.64m (Corrected by 1320 PWM nudge).
* **Stability Status:** The drone maintained a safe 7m flight envelope without manual intervention.

---

## 📁 Project Structure
* `hover_tune_mission.py`: Phase 2 precision mission script (1350 PWM).
* `waypoint_mission.py`: Original Phase 1 high-altitude script.
* `/telemetry_logs`: Contains CSV data for both successful flight phases.
* `requirements.txt`: Python dependencies (DroneKit & SITL).

## 🛠️ Technical Specifications
- **Language:** Python 3.9
- **Simulator:** DroneKit-SITL (ArduCopter V3.3)
- **Control Strategy:** Guided Mode with Manual PWM Channel Overrides.
- **Next Step (Phase 3):** Implementation of a PID Controller for perfect altitude locking.

---
*Developed by Pradhyumna Avinash Ramgirwar (2026)*
