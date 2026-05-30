# YOLO-Based-Intelligent-Traffic-Signal-Management-System
<p align="justify">
Traffic congestion is a persistent challenge in urban areas, and conventional traffic signal systems with fixed timing often fail to adapt to real-time conditions. This project presents an <b>AI-Based Traffic Signal Management System</b> that leverages <b>YOLOv8</b> for real-time vehicle detection and counting across multiple lanes. Based on the computed traffic density, the system dynamically regulates signal timings, ensuring a more efficient traffic flow, reduced congestion, and minimized waiting time.
</p>

## Features
* Real-time Vehicle Detection: Uses YOLOv8 to detect vehicles from live video feeds with high accuracy.
* Multi-Lane Monitoring: Simultaneously processes and analyzes traffic across four different lanes.
* Dynamic Signal Control: Automatically adjusts traffic light timings based on real-time vehicle density.
* Vehicle Classification: Identifies and categorizes vehicles into cars, buses, trucks, and motorcycles.
* Live Dashboard: Provides an interactive GUI showing lane status, vehicle counts, and congestion levels.
* Traffic Density Visualization: Displays real-time graphs to analyze traffic flow trends.
* Congestion Alerts: Highlights heavily crowded lanes to indicate traffic congestion.
* Optimized Traffic Flow: Reduces waiting time by prioritizing busier lanes intelligently.

## Technologies Used
* **Python** – Core programming language for the system
* **OpenCV** – Video processing and frame handling
* **YOLOv8 (Ultralytics)** – Real-time object detection model
* **NumPy** – Numerical computations and data handling
* **Tkinter** – GUI development for the dashboard interface
* **Matplotlib** – Real-time traffic data visualization
* **Pillow (PIL)** – Image processing for displaying video frames in GUI

# Working Of the Project
<p align="justify">
The system processes real-time traffic from four designed lanes using YOLOv8 for vehicle detection and counting. The traffic signal starts from the first lane and follows a continuous circular loop across all four lanes. Based on the detected vehicle density, each lane is assigned a dynamic green signal duration within a fixed range of 5 seconds (minimum) to 20 seconds (maximum), ensuring adaptive traffic control. Before switching to the next lane, a yellow signal is displayed for 2 seconds to ensure smooth transition. Lanes with higher traffic density are allocated longer green time, while less congested lanes receive shorter durations, resulting in optimized traffic flow and reduced congestion
</p>

<h3>How to run the Project</h3>
📥 1. Clone the Repository
Begin by cloning the repository from GitHub:
<pre><code>
git clone https://github.com/your-username/AI-Traffic-Signal-Management-System.git
cd AI-Traffic-Signal-Management-System 
</code></pre>

🤖 2. Setup YOLOv8 Model

This project uses the YOLOv8 pre-trained model (yolov8s.pt) for real-time vehicle detection.

The model file is already included in the repository itself
Make sure yolov8s.pt is present in the project directory after cloning

Install the required dependency:
pip install ultralytics
🎥 3. Add Traffic Video Inputs

Download four clear traffic videos representing different road conditions. These videos simulate the four traffic lanes.

Rename them exactly as follows and place them in the project folder:
traffic_01.mp4
traffic_02.mp4
traffic_03.mp4
traffic_04.mp4
⚠️ Ensure the videos are clear for accurate vehicle detection and analysis.
📦 4. Install Dependencies

Install all required Python libraries:
pip install opencv-python numpy pillow matplotlib
🚀 5. Run the Application
python main.py


