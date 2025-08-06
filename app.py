import os
from keras.models import load_model
import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='static')

# Load Emotion Detection Model (ONCE)
emotion_model = None
try:
    MODEL_PATH = os.path.join('face_model.h5')  # Adjust path if in subfolder
    emotion_model = load_model(MODEL_PATH)
    print("✅ Emotion detection model loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load emotion model: {e}")

# Emotion Labels and Emoji Map
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
emoji_map = {
    'Angry': '😠', 'Disgust': '🤢', 'Fear': '😨', 'Happy': '😄',
    'Sad': '😢', 'Surprise': '😮', 'Neutral': '😐'
}

# Preprocess image for model
def preprocess_image(image_base64):
    try:
        image_data = base64.b64decode(image_base64.split(',')[1])
        image = Image.open(BytesIO(image_data)).convert('L')  # grayscale
        image = image.resize((48, 48))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=(0, -1))  # (1, 48, 48, 1)
        return image
    except Exception as e:
        print(f"⚠️ Error during preprocessing: {e}")
        return None

# ROUTES

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/system')
def system_page():
    return render_template('system.html')

@app.route('/emotion_page')
def emotion_page():
    return render_template('emotion.html')

@app.route('/structure_page')
def structure_page():
    return render_template('structure.html')

@app.route('/skin_page')
def skin_page():
    return render_template('skin.html')

@app.route('/emotion', methods=['POST'])
def detect_emotion():
    if not emotion_model:
        return jsonify({'error': 'Model not loaded'}), 500

    data = request.get_json()
    image = preprocess_image(data.get('image', ''))

    if image is None:
        return jsonify({'error': 'Invalid image data'}), 400

    try:
        prediction = emotion_model.predict(image)[0]
        label = emotion_labels[np.argmax(prediction)]
        return jsonify({'label': label, 'emoji': emoji_map[label]})
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return jsonify({'error': 'Prediction failed'}), 500

@app.route('/structure', methods=['POST'])
def detect_structure():
    return jsonify({'label': 'Oval (Example)'})

@app.route('/skin', methods=['POST'])
def detect_skin_type():
    return jsonify({'label': 'Oily Skin (Example)'})

# Entry point
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
