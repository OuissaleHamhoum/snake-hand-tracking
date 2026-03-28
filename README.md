# 🐍 Nokia Snake Hand Tracking Game

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.9.0-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.7-orange.svg)](https://mediapipe.dev/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/OuissaleHamhoum/snake-hand-tracking.svg)](https://github.com/OuissaleHamhoum/snake-hand-tracking/stargazers)

> **Control the classic Snake game with your hand gestures using Computer Vision!**  
> No keyboard, no mouse - just your hand movements captured by your webcam.

---

## ✨ Features

- 🖐️ **Hand Gesture Control** - Move the snake by simply moving your hand
- 🎵 **Immersive Audio** - Background music and sound effects for actions
- 📈 **5 Progressive Levels** - Difficulty increases as you advance
- 🎨 **Colorful Food System** - Random colored food items for visual variety
- 🏆 **Score & Level Tracking** - Real-time scoring and level progression
- 🖥️ **Real-time Camera View** - See yourself controlling the game
- 🎯 **Responsive Controls** - Smooth hand tracking with MediaPipe

---

## 🎯 How It Works

The game uses computer vision to track your hand movements:

1. **Hand Detection** - MediaPipe detects 21 hand landmarks in real-time
2. **Direction Control** - Vector between wrist and index finger determines movement direction
3. **Gesture Commands** - Open palm to select, fist to quit
4. **Game Mechanics** - Classic Snake gameplay with modern controls

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Webcam
- Git (optional, for cloning)

### Installation

```bash
# Clone the repository
git clone https://github.com/OuissaleHamhoum/snake-hand-tracking.git
cd snake-hand-tracking

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
