from flask import Flask, render_template, request, send_file, send_from_directory
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
AUDIO_FOLDER = "static/audio"

# Create folder if it doesn't exist
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speak', methods=['POST'])
def speak():
    text = request.form['text']
    if not text.strip():
        return "Please enter some text.", 400

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_FOLDER, filename)
    tts = gTTS(text=text, lang='en')
    tts.save(filepath)

    # Pass filename to frontend
    return render_template('index.html', audio_file=filename)

@app.route('/static/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
