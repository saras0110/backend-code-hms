from flask import Flask, render_template, request, jsonify
import cv2
from keras.models import load_model
import numpy as np
import datetime
import os
from PIL import Image
import io

app = Flask(__name__)

# Load face detector and emotion model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = load_model('face_model.h5')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Store logs in memory
emotion_log = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    img = Image.open(io.BytesIO(file.read())).convert('RGB')
    open_cv_image = np.array(img)
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    results = []
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48))
        roi_gray = roi_gray.astype('float') / 255.0
        roi_gray = np.expand_dims(roi_gray, axis=0)
        roi_gray = np.expand_dims(roi_gray, axis=-1)

        preds = model.predict(roi_gray)[0]
        emotion_probability = np.max(preds)
        emotion_label = emotion_labels[preds.argmax()]

        emotion_log.append({
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'emotion': emotion_label
        })

        results.append({
            'emotion': emotion_label,
            'confidence': float(emotion_probability)
        })

    return jsonify({'results': results})

@app.route('/logs')
def logs():
    return jsonify(emotion_log)

@app.route('/stats')
def stats():
    counts = {label: 0 for label in emotion_labels}
    for log in emotion_log:
        counts[log['emotion']] += 1
    return jsonify(counts)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
