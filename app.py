from flask import Flask, render_template, Response, jsonify
import cv2
from keras.models import load_model
import numpy as np
import datetime
import json
import os

app = Flask(__name__)

# Load face detector and emotion model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = load_model('emotion_model.h5')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Store logs in memory for now
emotion_log = []

camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                roi_gray = cv2.resize(roi_gray, (48, 48))
                roi_gray = roi_gray.astype('float') / 255.0
                roi_gray = np.expand_dims(roi_gray, axis=0)
                roi_gray = np.expand_dims(roi_gray, axis=-1)
                
                preds = model.predict(roi_gray)[0]
                emotion_probability = np.max(preds)
                emotion_label = emotion_labels[preds.argmax()]
                
                cv2.putText(frame, emotion_label, (x, y-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                emotion_log.append({
                    'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'emotion': emotion_label
                })
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/logs')
def logs():
    return jsonify(emotion_log)

@app.route('/stats')
def stats():
    counts = {label: 0 for label in emotion_labels}
    for log in emotion_log:
        counts[log['emotion']] += 1
    return render_template('stats.html', counts=counts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

