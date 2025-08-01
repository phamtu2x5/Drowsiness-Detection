from flask import Flask, render_template, Response, jsonify, request
import cv2
import numpy as np
from ultralytics import YOLO
import base64
import io
from PIL import Image
import signal
import sys
import atexit

app = Flask(__name__)

# Load model
model_path = 'runs/train/exp2_m_20_cur_best/weights/best.pt'
try:
    model = YOLO(model_path)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")

# Global variables
is_detecting = False
current_result = None

class_names = ['dog','person','cat','tv','car','meatballs','marinara sauce',
'tomato soup','chicken noodle soup','french onion soup','chicken breast',
'ribs','pulled pork','hamburger','cavity','awake','drowsy']

def cleanup_resources():
    """Cleanup all resources when app stops"""
    global is_detecting
    print("Cleaning up resources...")
    
    # Stop detection
    is_detecting = False
    
    # Clear model from memory
    if 'model' in globals():
        del model
        print("Model cleared from memory")
    
    print("Cleanup completed")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\nReceived interrupt signal. Shutting down gracefully...")
    cleanup_resources()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Register cleanup function
atexit.register(cleanup_resources)

def detect_drowsiness(frame):
    """Detect drowsiness in a frame"""
    if frame is None:
        print("Error: Frame is None")
        return None, []
    
    print(f"Frame shape: {frame.shape}")
    # Resize frame to smaller size for M2 optimization
    frame_resized = cv2.resize(frame, (320, 240))  # Smaller size for M2
    
    # Use lighter settings for M2
    try:
        results = model(frame_resized, conf=0.5, iou=0.4, verbose=False)
        result_img = results[0].plot()
        print(f"Detections found: {len(results[0].boxes)}")
    except Exception as e:
        print(f"Error in detection: {e}")
        return frame, []  # Return original frame with no detections
    
    # Resize back to original size
    result_img = cv2.resize(result_img, (frame.shape[1], frame.shape[0]))
    
    # Get detection results
    detections = []
    for r in results:
        boxes = r.boxes
        if boxes is not None:
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = class_names[cls]
                detections.append({
                    'class': class_name,
                    'confidence': conf,
                    'bbox': box.xyxy[0].tolist()
                })
    
    return result_img, detections

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_detection')
def start_detection():
    global is_detecting
    is_detecting = True
    return jsonify({'status': 'success', 'message': 'Detection started'})

@app.route('/stop_detection')
def stop_detection():
    global is_detecting, current_result
    print("Stopping detection...")
    
    is_detecting = False
    current_result = None
    print("Current result cleared")
    
    print("Detection stopped successfully")
    return jsonify({'status': 'success', 'message': 'Detection stopped'})

@app.route('/get_detection_result')
def get_detection_result():
    global current_result
    print(f"Getting detection result: {current_result}")  # Debug
    if current_result is None:
        return jsonify({'detections': []})
    
    # Filter for drowsiness-related classes
    drowsiness_detections = [d for d in current_result 
                           if d['class'] in ['awake', 'drowsy']]
    
    return jsonify({'detections': drowsiness_detections})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Read image
    image_bytes = file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return jsonify({'error': 'Invalid image data'}), 400
    
    # Perform detection
    result_img, detections = detect_drowsiness(img)
    
    if result_img is None:
        return jsonify({'error': 'Detection failed'}), 500
    
    # Convert result to base64
    ret, buffer = cv2.imencode('.jpg', result_img, [
        cv2.IMWRITE_JPEG_QUALITY, 60,
        cv2.IMWRITE_JPEG_OPTIMIZE, 1
    ])
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    # Update current_result for /get_detection_result
    global current_result
    current_result = detections
    
    return jsonify({
        'result_image': img_base64,
        'detections': detections
    })

@app.route('/status')
def app_status():
    """Check app status"""
    global is_detecting, current_result
    status = {
        'is_detecting': is_detecting,
        'has_current_result': current_result is not None,
        'model_loaded': 'model' in globals()
    }
    return jsonify(status)

@app.route('/cleanup', methods=['POST'])
def force_cleanup():
    """Force cleanup all resources"""
    cleanup_resources()
    return jsonify({'status': 'success', 'message': 'Cleanup completed'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)