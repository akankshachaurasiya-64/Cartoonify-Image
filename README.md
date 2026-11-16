# 🎨 Cartoonify Image

Flask web app that converts photos into cartoon style using OpenCV.

**Live Demo:** https://cartoonify-image.onrender.com

## Features
- Classic and Painted (K-Means) styles
- Upload, preview and download
- Input validation

## Tech Stack
Python, OpenCV, NumPy, Flask

## Run Locally
```bash
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000

## How It Works
Adaptive threshold for edges + bilateral filter for smooth colors + K-Means for color reduction.
