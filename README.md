# AeroGuard-IQ: Autonomous Obstacle Avoidance via MAVLink

## 📌 Project Overview
Developed as part of my Master’s in Electrical Engineering (OVGU), this project implements a reactive obstacle avoidance system for autonomous UAVs. The system interfaces with **ArduCopter V3.3** using Python to move beyond simple GPS waypoints into real-time sensor-based navigation.

## 🚀 Key Features
* **MAVLink Packet Injection:** Bypassed high-level API limitations by sending raw MAV_CMD packets for arming and takeoff.
* **Reactive Control Loop:** Implemented a 1Hz sense-act loop that triggers emergency braking ($V_x, V_y, V_z = 0$) if obstacles are detected within 7 meters.
* **Fail-Safe Telemetry:** Developed robust logic to handle `NoneType` sensor data, preventing script crashes during signal intermittent states.

## 📊 Development Phases
| Phase | Focus | Status |
| :--- | :--- | :--- |
| 1 | Environment Setup (SITL & Python 3.9) | Completed |
| 2 | Telemetry Handshaking & Heartbeat | Completed |
| 3 | MAVLink Command Logic & Parameter Tuning | Completed |
| 4 | **System Integration & Stress Testing** | **Finalized** |
| 5 | **Autonomous Obstacle Avoidance Logic** | **Verified** |

## 🛠 Engineering Challenges & Troubleshooting
The primary challenge involved a documented limitation in the legacy ArduCopter SITL firmware. In "headless" simulation modes, the **EKF (Extended Kalman Filter)** frequently experiences variance spikes during autonomous arming. 

**My Solution:** I implemented a pre-flight "Bulletproof Check" that waits for explicit hardware alignment before firing takeoff commands, successfully stabilizing the initial flight sequence despite firmware-level physics reboots.

---
