import io
import os
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify
import tensorflow as tf

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins (safe for development)


# Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model/my_model.h5')
model = tf.keras.models.load_model(MODEL_PATH)

# List of class names: Indian monument categories (must match training order)
class_names = [
    'Ajanta Caves', 'Charar-E- Sharif', 'Chhota_Imambara', 'Ellora Caves',
    'Fatehpur Sikri', 'Gateway of India', 'Humayun_s Tomb', 'India gate pics',
    'Khajuraho', 'Sun Temple Konark', 'alai_darwaza', 'alai_minar',
    'basilica_of_bom_jesus', 'charminar', 'golden temple', 'hawa mahal pics',
    'iron_pillar', 'jamali_kamali_tomb', 'lotus_temple', 'mysore_palace',
    'qutub_minar', 'tajmahal', 'tanjavur temple', 'victoria memorial'
]

def preprocess_image(image, target_size=(300, 300)):
    # Convert to RGB, resize, and scale between 0-1
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = image.resize(target_size)
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # batch dimension
    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    # Check if file included in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        image = Image.open(io.BytesIO(file.read()))
        processed_image = preprocess_image(image)
        predictions = model.predict(processed_image)
        pred_index = int(np.argmax(predictions, axis=1)[0])
        pred_class = class_names[pred_index]
        confidence = float(np.max(predictions))
        return jsonify({
            'prediction': pred_class,
            'confidence': confidence
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
