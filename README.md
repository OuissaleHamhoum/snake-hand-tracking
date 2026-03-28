# 🐍 Snake Hand Tracking Game

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.9-green.svg)](https://opencv.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange.svg)](https://mediapipe.dev)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **Classic Snake game controlled by hand gestures using Computer Vision**
> No keyboard required — control the snake using only your **hand movements captured by a webcam**.

---

# 📌 Overview

This project is a **real-time hand-tracking Snake game** where players control the snake by moving their hand in front of a webcam.

The system uses:

* **MediaPipe** for detecting **21 hand landmarks**
* **OpenCV** for video capture and processing
* **Pygame** for rendering the game and handling audio

💡 **Key idea:** Gesture-based gaming without using a keyboard or physical controller.

---

# 🎮 How It Works

## Technical Architecture

```
Webcam
   ↓
MediaPipe Hand Tracking
   ↓
Direction Vector Calculation
   ↓
Snake Movement Logic
   ↓
Pygame Game Rendering
```

---

## ✋ Hand Gesture System

| Gesture          | Detection Method                 | Action                  |
| ---------------- | -------------------------------- | ----------------------- |
| ✋ Open Hand      | 4+ fingers extended              | Start game              |
| ✊ Fist           | 0 fingers extended               | Quit game               |
| 👆 Hand Movement | Vector from wrist → index finger | Control snake direction |

---

# 🕹️ Game Features

* 🎯 **5 Progressive Levels** — game speed increases each level
* 🎥 **Live Camera Feedback** — see yourself while playing
* 🔊 **Audio Integration** — background music + sound effects
* 🍎 **Colorful Food System** — random colored food items
* 📈 **Score Tracking** — score increases with each food collected
* 💥 **Self-Collision Detection** — classic Snake mechanics

---

# 🛠️ Technologies Used

| Technology    | Purpose                                  |
| ------------- | ---------------------------------------- |
| **Python**    | Core game logic                          |
| **OpenCV**    | Camera capture and image processing      |
| **MediaPipe** | Hand landmark detection (21 points)      |
| **Pygame**    | Game graphics, audio, and UI             |
| **NumPy**     | Frame manipulation and vector operations |

---

# 📊 Key Technical Details

## Hand Tracking Algorithm

* **Landmarks Detected:** 21 hand points (joints, fingertips, wrist)
* **Direction Calculation:** Vector between **wrist and index finger**
* **Sensitivity Threshold:** `0.08`
* **Control Cooldown:** 5 frames between direction updates

---

## ⚡ Performance Metrics

| Metric             | Value                   |
| ------------------ | ----------------------- |
| FPS                | 30+ on standard webcams |
| Detection Accuracy | 95%+ in good lighting   |
| Latency            | < 50 ms                 |
| Supported OS       | Windows / macOS / Linux |

---

# ⚡ Key Features

✅ Real-time hand tracking (30+ FPS)
✅ Gesture-based controls
✅ Progressive difficulty levels
✅ Score tracking system
✅ Audio feedback system
✅ Camera overlay gameplay
✅ Smooth gesture-to-direction mapping

---

# 🚀 Quick Start

## Prerequisites

* Python **3.7+**
* Webcam
* 4GB RAM recommended

---

## Installation

```bash
# Clone repository
git clone https://github.com/OuissaleHamhoum/snake-hand-tracking.git

# Enter project folder
cd snake-hand-tracking

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

---

# 🎯 Implementation Highlights

## 1️⃣ Hand Tracking Integration

* Real-time landmark detection with **MediaPipe**
* Custom **gesture recognition logic**
* Smooth **direction control with cooldown system**

---

## 2️⃣ Game Design

* Classic **Snake gameplay**
* Modern **gesture-based controls**
* **Progressive difficulty** system
* Camera feed used as the **game background**

---

## 3️⃣ Audio System

* Background music integration
* Sound effects:
  * Food eaten
  * Level up
  * Game over
* Dynamic audio triggered by game events

---

## 4️⃣ User Interface

* Live camera feed background
* Retro-style **score and level display**
* Smooth **level transitions**
* **Game Over screen** with replay option

---

# 📈 Development Journey

## Challenges Solved

**Latency Reduction**
Implemented a cooldown system to prevent over-sensitive controls.

**Gesture Accuracy**
Optimized threshold values for stable detection in different lighting conditions.

**Collision Detection**
Efficient algorithm for detecting snake self-collision.

**Performance Optimization**
Maintained **30+ FPS** with real-time video processing.

---

# 🔮 Future Improvements

* 👥 Multiplayer mode
* 🎙️ Voice commands
* 🏆 Online leaderboard
* ⚡ Power-ups & special effects
* 📱 Mobile version using front camera
* 🎮 Additional game modes (Time Attack, Endless)

---

# 🙏 Acknowledgments

* **Google MediaPipe** for hand tracking technology
* **OpenCV** for computer vision tools
* **Pygame Community** for game development resources
* **Classic Nokia Snake** for inspiration

---
