# AeroGuard-IQ: Autonomous Drone Navigation System
**Master's Project (EEIT) - Otto von Guericke University Magdeburg**

## 🚀 Project Status: Phase 2 Complete (100%)
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
