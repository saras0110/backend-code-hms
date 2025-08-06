import os
from keras.models import load_model
import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/emotion_page')
def emotion_page():
    return render_template('emotion.html')

@app.route('/structure_page')
def structure_page():
    return render_template('structure.html')

@app.route('/skin_page')
def skin_page():
    return render_template('skin.html')

# Load Emotion Detection Model
try:
    MODEL_PATH = os.path.join('models', 'face_model.h5')
    emotion_model = load_model(MODEL_PATH)
except Exception as e:
    print(f"⚠️ Failed to load emotion model: {e}")
    emotion_model = None

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
emoji_map = {
    'Angry': '😠', 'Disgust': '🤢', 'Fear': '😨', 'Happy': '😄',
    'Sad': '😢', 'Surprise': '😮', 'Neutral': '😐'
}

def preprocess_image(image_base64):
    image_data = base64.b64decode(image_base64.split(',')[1])
    image = Image.open(BytesIO(image_data)).convert('L')
    image = image.resize((48, 48))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=(0, -1))
    return image

@app.route('/emotion', methods=['POST'])
def detect_emotion():
    if emotion_model is None:
        return jsonify({'error': 'Emotion model not loaded'}), 500

    data = request.get_json()
    image = preprocess_image(data['image'])
    prediction = emotion_model.predict(image)[0]
    label = emotion_labels[np.argmax(prediction)]
    return jsonify({'label': label, 'emoji': emoji_map[label]})

@app.route('/structure', methods=['POST'])
def detect_structure():
    return jsonify({'label': 'Oval (Example)'})

@app.route('/skin', methods=['POST'])
def detect_skin_type():
    return jsonify({'label': 'Oily Skin (Example)'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
