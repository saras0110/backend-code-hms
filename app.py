from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from deepface import DeepFace
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

@app.route('/detect_emotion', methods=['POST'])
def detect_emotion():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    img = Image.open(file.stream).convert('RGB')
    img_np = np.array(img)

    try:
        result = DeepFace.analyze(img_path=img_np, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        return jsonify({"emotion": emotion})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Facial Emotion Detection Backend Running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
