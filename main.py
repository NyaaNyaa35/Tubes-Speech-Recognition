from flask import Flask, render_template, request
import speech_recognition as sr
import os

app = Flask(__name__)
@app.route("/")
def index(): 
    return render_template("index.html")

@app.route('/process', methods=['GET', 'POST'])
def process():
    r = sr.Recognizer()
    audio = False
    response = ""
    if request.method == 'POST':
        save_path = os.path.join("", "audio.wav")
        request.files['audio_data'].save(save_path)
    
        with sr.AudioFile('audio.wav') as source:
            audio = r.record(source)
            try:
                response = r.recognize_google(audio)
                print("Text: "+response)
            except Exception as e:
                print("Exception: "+str(e))
                
    return response

    

if __name__ == "__main__":
    app.run(debug=True)