from flask import Flask, request, render_template, jsonify
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
import random
import string

app = Flask(__name__)


MODEL_PATH = 'model.h5'

def encrypt(text: str) -> str:
    encrypted_text = ""
    
    for char in text:
        if char.isalpha():  
            shifted_char = chr(((ord(char) - (65 if char.isupper() else 97) + 3) % 26) + (65 if char.isupper() else 97))
            random_chars = ''.join(random.choices(string.ascii_letters, k=2))
            encrypted_text += shifted_char + random_chars
        elif char == ' ':
            encrypted_text += 'AsqE'
    
    return encrypted_text

def decryptText(encrypted_text: str) -> str:
    decrypted_text = ""
    i = 0
    
    while i < len(encrypted_text):
        if encrypted_text[i:i+4] == "AsqE":
            decrypted_text += " "
            i += 4  
        elif encrypted_text[i].isalpha():  
            original_char = chr(((ord(encrypted_text[i]) - (65 if encrypted_text[i].isupper() else 97) - 3) % 26) + (65 if encrypted_text[i].isupper() else 97))
            decrypted_text += original_char
            i += 3 
        else:
            i += 1 

    return decrypted_text

try:
    model = load_model(MODEL_PATH)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def preprocess_text(text):
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/decrypt", methods=['POST'])
def decrypt():
    try:
        data = request.get_json()
        input_text = data.get('text', '')
        
        if not input_text:
            return jsonify({'error': 'No text provided'}), 400

        # Preprocess the text
        processed_text = preprocess_text(input_text)
        
        result = decryptText(processed_text)
        
        return jsonify({
            'status': 'success',
            'prediction': result
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
       
        data = request.get_json()
        input_text = data.get('text', '')
        
        if not input_text:
            return jsonify({'error': 'No text provided'}), 400

   
        processed_text = preprocess_text(input_text)
        
       
        
        result = encrypt(processed_text)
        
        return jsonify({
            'status': 'success',
            'prediction': result
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)