import os
from flask import Flask, request, jsonify
from keras.models import load_model
import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Load Emotion Detection Model
try:
    emotion_model = load_model('face_model.h5')
except Exception as e:
    print(f"⚠️ Failed to load emotion model: {e}")
    emotion_model = None

# Placeholder: You can add real models later
# structure_model = load_model('facial_structure_model.h5')
# skin_model = load_model('skin_type_model.h5')

# Labels and Emoji mapping
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
emoji_map = {
    'Angry': '😠', 'Disgust': '🤢', 'Fear': '😨', 'Happy': '😄',
    'Sad': '😢', 'Surprise': '😮', 'Neutral': '😐'
}

# Preprocess input image
def preprocess_image(image_base64):
    image_data = base64.b64decode(image_base64.split(',')[1])
    image = Image.open(BytesIO(image_data)).convert('L')  # grayscale
    image = image.resize((48, 48))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=(0, -1))
    return image

# Route: Emotion Detection
@app.route('/emotion', methods=['POST'])
def detect_emotion():
    if emotion_model is None:
        return jsonify({'error': 'Emotion model not loaded'}), 500

    data = request.get_json()
    image = preprocess_image(data['image'])
    prediction = emotion_model.predict(image)[0]
    label = emotion_labels[np.argmax(prediction)]
    return jsonify({'label': label, 'emoji': emoji_map[label]})

# Route: Structure Detection (Dummy)
@app.route('/structure', methods=['POST'])
def detect_structure():
    return jsonify({'label': 'Oval (Example)'})

# Route: Skin Type Detection (Dummy)
@app.route('/skin', methods=['POST'])
def detect_skin_type():
    return jsonify({'label': 'Oily Skin (Example)'})

# Root route
@app.route('/')
def home():
    return "✅ Backend Running Successfully"

# Run app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
