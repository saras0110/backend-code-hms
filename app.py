from flask import Flask, request, jsonify
from keras.models import load_model
import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Load models
emotion_model = load_model('face_model.h5')
# structure_model = load_model('facial_structure_model.h5')
# skin_model = load_model('skin_type_model.h5')

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
def emotion():
    data = request.get_json()
    image = preprocess_image(data['image'])
    prediction = emotion_model.predict(image)[0]
    label = emotion_labels[np.argmax(prediction)]
    return jsonify({'label': label, 'emoji': emoji_map[label]})

@app.route('/structure', methods=['POST'])
def structure():
    return jsonify({'label': 'Oval (Example)'})  # Add actual model and prediction here

@app.route('/skin', methods=['POST'])
def skin():
    return jsonify({'label': 'Oily Skin (Example)'})  # Add actual model and prediction here

@app.route('/')
def home():
    return "Backend Running Successfully"

if __name__ == '__main__':
     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
