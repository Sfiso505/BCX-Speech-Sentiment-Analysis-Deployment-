# Speech_Recognition_app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
from model_inference import load_trained_model, preprocess_audio, predict_emotion
import os
import numpy as np

app = Flask(__name__)

# Set the maximum content length for incoming requests to 32 megabytes
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

# Load the trained model during initialization
model = load_trained_model('entire_trained-model.h5')

emotion_labels = ['fear', 'angry', 'disgust', 'neutral', 'sad', 'surprise', 'happy', 'calm']

def process_audio_file(audio_file):
    # Preprocess the audio file
    audio_features = preprocess_audio(audio_file)

    # Perform model inference
    prediction = predict_emotion(model, audio_features)

    return prediction

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get the uploaded audio file
        audio_file = request.files['audio_file']
        if audio_file:
            # Save the audio file temporarily
            temp_path = 'temp_audio.wav'
            audio_file.save(temp_path)

            # Process the audio file and get the prediction
            result = process_audio_file(temp_path)

            # Remove the temporary audio file
            os.remove(temp_path)

            # Assuming 'result' is your prediction result
            predicted_emotion = emotion_labels[np.argmax(result)]

            return render_template('result.html', predicted_emotion=predicted_emotion)
        else:
            return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
