import cv2, numpy as np, time, tkinter as tk
from PIL import Image, ImageTk
from ultralytics import YOLO
from collections import deque

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# MODEL SETUP
model = YOLO("yolov8s.pt")

vehicle_classes = {"car", "truck", "bus", "motorcycle"}

colors = {
    "car": (0, 255, 0),
    "truck": (0, 0, 255),
    "bus": (255, 0, 0),
    "motorcycle": (0, 255, 255)
}

caps = [cv2.VideoCapture(f"traffic_0{i}.mp4") for i in range(1, 5)]
lane_names = [f"Lane {i}" for i in range(1, 5)]

history = [deque(maxlen=60) for _ in range(4)]
time_history = deque(maxlen=60)

signal_idx = 0
state = "GREEN"
t0 = time.time()

BASE, MAX, YELLOW = 5, 20, 3   # FIXED YELLOW TIME = 3 seconds

running = True
frame_skip = 3
frame_count = 0

last_counts = [0] * 4
last_type_counts = [dict.fromkeys(vehicle_classes, 0) for _ in range(4)]
last_boxes = [[] for _ in range(4)]

# GUI
root = tk.Tk()
root.title("AI-Based Traffic Signal Management System")
root.geometry("1600x900")

root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=2)
root.grid_rowconfigure(0, weight=1)

video_container = tk.Frame(root, bd=3, relief="ridge")
video_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

tk.Label(video_container, text="LIVE TRAFFIC FEED",
         font=("Times New Roman", 16, "bold")).pack()

video_frame = tk.Frame(video_container)
video_frame.pack()

labels = [tk.Label(video_frame) for _ in range(4)]
for i, l in enumerate(labels):
    l.grid(row=i // 2, column=i % 2, padx=10, pady=10)

dash_container = tk.Frame(root, bd=3, relief="ridge")
dash_container.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

tk.Label(dash_container, text="TRAFFIC DASHBOARD",
         font=("Times New Roman", 16, "bold")).pack()

lane_title = tk.Label(dash_container, font=("Times New Roman", 15, "bold"))
lane_title.pack(pady=5)

info_box = tk.Label(
    dash_container,
    font=("Times New Roman", 12, "bold"),
    justify="left",
    bd=2,
    relief="groove"
)
info_box.pack(fill="x", padx=10, pady=10)

graph_frame = tk.Frame(dash_container, bd=2, relief="groove")
graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

fig, ax = plt.subplots(figsize=(5,3))
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

status = tk.Label(root, font=("Times New Roman", 14, "bold"),
                  bd=2, relief="sunken")
status.grid(row=1, column=0, columnspan=2, sticky="ew")

# MAIN LOOP
def update():
    global signal_idx, state, t0, frame_count

    frame_count += 1
    frames, counts = [], [0]*4

    for i, cap in enumerate(caps):
        ok, frame = cap.read()

        if not ok:
            frames.append(np.zeros((300,400,3), np.uint8))
            continue

        if frame_count % frame_skip == 0:
            small = cv2.resize(frame, (640,360))
            sx, sy = frame.shape[1]/640, frame.shape[0]/360

            c = 0
            type_count = dict.fromkeys(vehicle_classes, 0)
            current_boxes = []

            results = model(small, conf=0.3, verbose=False)

            for r in results:
                for b in r.boxes:
                    label = model.names[int(b.cls[0])]

                    if label in vehicle_classes:
                        c += 1
                        type_count[label] += 1

                        x1,y1,x2,y2 = map(int, b.xyxy[0])
                        x1,y1,x2,y2 = int(x1*sx),int(y1*sy),int(x2*sx),int(y2*sy)

                        conf = float(b.conf[0])
                        color = colors[label]

                        current_boxes.append((x1,y1,x2,y2,label,conf,color))

            last_counts[i] = c
            last_type_counts[i] = type_count
            last_boxes[i] = current_boxes

        counts[i] = last_counts[i]
        history[i].append(counts[i])

        for (x1,y1,x2,y2,label,conf,color) in last_boxes[i]:
            cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)
            cv2.putText(frame,f"{label} {conf:.2f}",
                        (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,color,2)

        frames.append(frame)

    # TRAFFIC LOGIC
    avg = [sum(h)/len(h) if h else 0 for h in history]
    max_d = max(avg) if max(avg)>0 else 1
    ratio = avg[signal_idx]/max_d
    green_time = int(BASE + ratio*(MAX-BASE))

    elapsed = time.time() - t0

    if state == "GREEN" and elapsed >= green_time:
        state = "YELLOW"
        t0 = time.time()

    elif state == "YELLOW" and elapsed >= YELLOW:
        signal_idx = (signal_idx + 1) % 4
        state = "GREEN"
        t0 = time.time()

    # FIXED TIMER DISPLAY (IMPORTANT FIX)
    if state == "GREEN":
        rem = max(0, int(green_time - elapsed))
    else:  # YELLOW state
        rem = max(0, int(YELLOW - elapsed))

    # GRAPH UPDATE
    time_history.append(time.time())

    if frame_count % 5 == 0:
        ax.clear()
        ax.plot(list(time_history),
                list(history[signal_idx]),
                color="green", linewidth=2)

        ax.set_title("Traffic Density vs Time (Active Lane)")
        ax.set_xlabel("Time")
        ax.set_ylabel("Vehicles")
        ax.grid(True, linestyle="--", alpha=0.6)

        canvas.draw()
      
    # DISPLAY
    output = []

    for i, frame in enumerate(frames):

        light = (0,0,255)
        label = "RED"

        if i == signal_idx:
            if state == "GREEN":
                light = (0,255,0); label = "GREEN"
            elif state == "YELLOW":
                light = (0,255,255); label = "YELLOW"

        cv2.circle(frame,(40,40),15,light,-1)
        cv2.putText(frame,label,(70,45),
                    cv2.FONT_HERSHEY_SIMPLEX,0.6,light,2)

        if i == signal_idx and counts[i] > 20:
            cv2.putText(frame,"DENSE TRAFFIC!",
                        (120,80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,(0,0,255),3)

        if i != signal_idx:
            overlay = frame.copy()
            cv2.rectangle(overlay,(0,0),
                          (frame.shape[1],frame.shape[0]),
                          (0,0,0),-1)
            frame = cv2.addWeighted(overlay,0.3,frame,0.7,0)

        img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img).resize((400,300))
        output.append(ImageTk.PhotoImage(img))

    for i in range(4):
        labels[i].config(image=output[i])
        labels[i].image = output[i]

    
    # DASHBOARD
    active = signal_idx
    total = counts[active]
    breakdown = last_type_counts[active]

    lane_title.config(text=f"{lane_names[active]} — {state}")

    info_box.config(
        text=
        f"Total Vehicles: {total}\n\n"
        f"Car        : {breakdown['car']}\n"
        f"Bus        : {breakdown['bus']}\n"
        f"Truck      : {breakdown['truck']}\n"
        f"Motorcycle : {breakdown['motorcycle']}\n\n"
        f"{'🚨 CONGESTION ALERT' if total > 20 else 'Normal Traffic'}"
    )

    status.config(
        text=f"{lane_names[signal_idx]} | {state} | ⏳ {rem}s"
    )

    root.after(30, update)

# CONTROL
def start():
    global running
    running = True

def stop():
    global running
    running = False

tk.Button(root, text="START", bg="green", fg="white",
          command=start).grid(row=2, column=0)

tk.Button(root, text="STOP", bg="red", fg="white",
          command=stop).grid(row=2, column=1)

def close():
    for c in caps:
        c.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close)

update()
root.mainloop()
