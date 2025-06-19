# Virtual Shirt Try-On System

An interactive web-based virtual try-on system that allows users to virtually try on different shirts using AI-powered body tracking and gesture controls.

## Features

- Real-time virtual shirt try-on
- Gesture-based controls for intuitive interaction
- Multiple shirt options
- Size adjustment capabilities
- Responsive web interface
- Real-time body tracking and pose estimation

## Technologies Used

- **Frontend:**
  - HTML5
  - CSS3
  - JavaScript
  - WebSocket for real-time communication

- **Backend:**
  - Python
  - Flask (Web Server)
  - WebSocket Server
  - OpenCV
  - MediaPipe for pose estimation and hand tracking

## Prerequisites

- Python 3.7 or higher
- Webcam
- Modern web browser (Chrome/Firefox recommended)
- Node.js and npm (for development)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Virtual-shirt-Try-On.git
   cd Virtual-shirt-Try-On

2. Install Python dependencies:
   ```bash
   pip install opencv-python mediapipe numpy websockets asyncio flask
   
## Running the Application
1. Start the Flask server:
   
   ```
   python server.py
   ```
2. In a new terminal, start the WebSocket server:
   
   ```
   python websocket_server.py
   ```
3. Open your web browser and navigate to:
   
   ```
   http://localhost:5000
   ```
## Gesture Controls
- Thumb-Index Pinch: Increase shirt size
- Middle-Ring Pinch: Decrease shirt size
- Index-Middle Pinch: Change shirt

## Technical Architecture
The system uses a multi-stage pipeline:

1. Real-time webcam feed processing
2. Body pose estimation using MediaPipe
3. Hand gesture recognition
4. Shirt overlay and size adjustment
5. Real-time rendering

## Acknowledgments
- MediaPipe for providing the pose estimation framework
- OpenCV community for computer vision tools
- Flask and WebSocket for enabling real-time web communication
