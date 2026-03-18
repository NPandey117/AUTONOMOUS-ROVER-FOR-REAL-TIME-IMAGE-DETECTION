import cv2
import time
from flask import Flask, render_template, Response, jsonify
from ultralytics import YOLO
from picamera2 import Picamera2

app = Flask(__name__)

print("Loading YOLO NCNN model...")
# Ensure this path is correct for your Raspberry Pi
model = YOLO('/home/pi/yolo/best_model_ncnn_model_extracted/best_model_ncnn_model', task='detect')

start_time = time.time()
detected_cards = set()

print("Initializing camera...")
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(config)
picam2.start()

def generate_frames():
    global detected_cards
    
    while True: 
        # Capture frame
        frame = picam2.capture_array()
        # Convert RGB (PiCamera) to BGR (OpenCV)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
       
        # Run Inference
        results = model.predict(frame_bgr, stream=True, verbose=False)
        
        for r in results:
            for box in r.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = model.names[class_id]
               
                if confidence > 0.50:
                    detected_cards.add(class_name)
               
                # Draw Box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame_bgr, (0, 255, 0), 2)
                cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
               
                label = f"{class_name} ({confidence:.2f})"
                cv2.putText(frame_bgr, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
           
        # Encode as JPEG after all boxes are drawn
        ret, buffer = cv2.imencode('.jpg', frame_bgr)
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_stats')
def get_stats():
    elapsed = int(time.time() - start_time)
    minutes, seconds = divmod(elapsed, 60)
    time_str = f"{minutes:02d}:{seconds:02d}"
    
    return jsonify({
        'cards_detected': len(detected_cards),
        'time_elapsed': time_str,
        'detected_names': list(detected_cards)
    })

@app.route('/reset', methods=['POST'])
def reset():
    global start_time, detected_cards
    start_time = time.time()
    detected_cards.clear()
    return jsonify({'status': 'Memory wiped. Timer reset.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
