# AUTONOMOUS-ROVER-FOR-REAL-TIME-IMAGE-DETECTION
An autonomous vehicle featuring a dual-controller architecture (Raspberry Pi &amp; ESP32) for real-time path navigation and CV-based object identification. The system executes onboard YOLO inference for identification of 16 targets and manages dynamic obstacle avoidance within certain defined constraints.

Overview
The project implements a fully autonomous rover engineered for the Kriti 2026 Inter-Hostel Tech Competition. Designed with a dual-controller architecture, the system integrates a Raspberry Pi 4 for high-level computer vision and an Arduino Uno for precise, real-time mechatronic control. The rover is tasked with navigating complex symmetric paths, avoiding dynamic obstacles, and identifying 16 unique image cards using an onboard YOLO-based perception pipeline.

Key Features
Heterogeneous Processing: Utilizes a Raspberry Pi 4 (8GB) for vision and a Flask-based web server, while an Arduino Uno handles low-latency PID line following and sensor polling.
Onboard Perception: Implements a lightweight YOLO Nano model (yolo26n.pt) optimized into NCNN format for high-speed edge inference on the Raspberry Pi.Adaptive Navigation: Employs a 5-channel IR sensor array with a PID control loop ($K_p=2, K_d=14$) for smooth path tracking and a last-seen memory function for line recovery.
Dynamic Vision Scanning: Features an ultrasonic-triggered servo mechanism that rotates the camera module to track and identify image cards on either side of the track.
Real-time Telemetry: A custom web dashboard provides a live MJPEG camera feed, detected card logs, confidence scores, and a mission timer via a Wi-Fi-enabled Flask interface.

System Architecture
The robot operates across four modular layers to ensure stable performance:
Sensing Layer: 5-channel IR array for pathing and dual ultrasonic sensors for card/obstacle detection.
Processing Layer: Arduino (PID & Actuation) + Raspberry Pi (YOLO Inference & Web Server).
Actuation Layer: L298N Motor Driver powering 12V DC motors and an MG995 servo for camera positioning.
Visualization Layer: Flask-based web interface for remote mission monitoring.

Repository Structure

The project is organized into modular directories to separate hardware design, embedded firmware, and high-level perception logic.

```text
AUTONOMOUS-ROVER-FOR-REAL-TIME-IMAGE-DETECTION/
├── hardware/              # Mechatronic design and power distribution
│   ├── schematic.pdf      # Circuit diagrams designed in EasyEDA 
│   └── bom.md             # Detailed Bill of Materials (BOM) 
├── software/              # Embedded control and CV pipeline 
│   ├── firmware/          # Low-latency Arduino PID and sensor logic 
│   ├── app.py             # Flask-based YOLO inference engine and telemetry server 
│   └── index.html         # Real-time WebSocket dashboard for live telemetry 
├── docs/                  # Technical documentation 
│   ├── report.pdf         # Control theory, vision architecture, and logic flow 
│   └── presentation.pdf   # Technical design review (TDR) slides 
├── media/                 # Performance validation 
│   ├── demo_video.mp4     # Full-course autonomous navigation recording 
│   └── screenshots/       # GUI captures and hardware integration photos 
├── .gitignore             # Version control exclusions
├── README.md              # Project specifications and deployment guide
└── requirements.txt       # Python dependency manifest (OpenCV, Flask, etc.)
```
Technical Specifications

The following table summarizes the core technical parameters and design constraints of the system.

| Category | Specification | Details |
| :--- | :--- | :--- |
| **Primary Controller** | Raspberry Pi 4 Model B (8GB) | [cite_start]Handles YOLO inference, Flask server, and CSI camera  |
| **Secondary Controller**| Arduino Uno | Manages PID line-following, IR polling, and PWM  |
| **Vision Model** | YOLO Nano (yolo26n.pt) | Trained for 100 epochs; optimized to NCNN format |
| **Input Resolution** | 640 X 640 pixels | Standardized for consistent real-time detection |
| **Navigation Logic** | PID Control Loop | Parameters: Kp=2, Kd=14 (Non-blocking) |
| **Sensing** | IR Array & Ultrasonic | TCRT5000 (5-Ch) & HC-SR04 for obstacle/card detection |
| **Actuation** | DC Motors & MG995 Servo | Differential drive with a 360 deg rotating camera |
| **Power System** | 11.1V Li-Po (3S) | Buck Converter (5V Standard) |
| **Physical Limits** | 25 X 25 X 25 cm_cubed | Optimized to meet strict arena volume constraints |
| **Weight** | < 3 kg | Lightweight chassis design for maximum mobility  |
| **Dashboard** | Flask Web Interface | Live MJPEG stream, telemetry, and mission timer |


Installation & Usage
1. Firmware Deployment:Connect the Arduino Uno to your PC.Upload the control code found in software/firmware/ using the Arduino IDE.
2. Software Setup:Flash Raspberry Pi OS and ensure the camera CSI interface is enabled.Navigate to the project directory and install dependencies:
   Bash
   pip install -r requirements.txt
3. Launch the vision server:
   Bash
   python3 app.py
4. Operation:Access the dashboard at http://<raspberry_pi_ip>:5000.Place the rover on the track and power the 11.1V system to begin autonomous navigation.
