# CyberHUD V2: Touchless AR Interface 🦾

> A futuristic, cyberpunk-inspired Augmented Reality interface powered by computer vision.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Computer Vision](https://img.shields.io/badge/View-OpenCV-green?style=for-the-badge&logo=opencv&logoColor=white)
![Tracking](https://img.shields.io/badge/Model-MediaPipe-orange?style=for-the-badge&logo=google&logoColor=white)

## 🌟 Overview
**CyberHUD** allows users to interact with digital elements using only hand gestures. Unlike basic hand trackers that look for simple static poses (like a "thumbs up"), this project implements a **continuous physics-based interaction system**.

It features a "Bio-Energy" mechanic where the geometry and visuals of the HUD evolve in real-time based on the contraction of the user's hand (calculating contour area to drive animation states from 0.0 to 1.0).

## 🚀 Key Features
* **Continuous State Tracking**: "Squeeze" detection calculates hand contour area to drive fluid animation states rather than binary on/off switches.
* **Motion Trails**: Deque-based coordinate buffering creates fluid light trails for fingertips (Sci-Fi motion blur).
* **Procedural Geometry**: Orbital rings and HUD elements generate procedurally based on "Energy" levels.
* **Adaptive Bloom**: Real-time alpha blending simulates neon light diffusion for a "Cyberpunk" aesthetic.
* **Optimized Rendering**: Runs at 30+ FPS on standard CPU hardware.

## 💡 Real-World Applications
This prototype demonstrates the core technology used in:
* **🏥 Sterile Medical Interfaces**: Allowing surgeons to manipulate X-rays/data without touching non-sterile screens.
* **🏭 Smart Kiosks**: Touchless interaction for public terminals (ATMs, Ticketing) to improve hygiene.
* **👓 AR/VR Headsets**: Controller-free input systems similar to Apple Vision Pro or Meta Quest.

## 🛠️ Installation

### Prerequisites
* Python 3.10 or 3.11
* A working Webcam

### Setup
1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/cyber-hand-ar.git](https://github.com/YOUR_USERNAME/cyber-hand-ar.git)
    cd cyber-hand-ar
    ```

2.  **Create a Virtual Environment**
    ```bash
    # Windows
    py -3.10 -m venv ar_env
    ar_env\Scripts\activate

    # Mac/Linux
    python3.10 -m venv ar_env
    source ar_env/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install opencv-python mediapipe numpy
    ```

## 🎮 How to Use
Run the main script:
```bash
python cyber_hand.py

### Controls & Gestures

| Gesture | Action | Visual Effect |
| :--- | :--- | :--- |
| **Open Palm** | **Idle Mode** | Scanner active, Motion trails enabled on fingertips. |
| **Squeeze (50%)** | **Arming** | Orbital rings deploy, "SYSTEM ARMED" alert triggers. |
| **Fist (100%)** | **Max Power** | Core bloom reaches maximum intensity, HUD bars fill completely. |
| **ESC Key** | **Exit** | Quits the application. |

### 🧠 Technical Implementation
* **Smoothing**: Implements custom smoothing algorithms to reduce MediaPipe landmark jitter.
* **Vector Math**: Uses Euclidean distance and Contour Area calculation for gesture recognition (avoiding hard-coded thresholds).
* **Performance**: Optimized `cv2` drawing calls to minimize latency during the render loop.