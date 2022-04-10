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
    r.energy_threshold = 4000 # biar kedengeran oleh micnya
    r.dynamic_energy_threshold = True 
    r.dynamic_energy_adjustment_damping = 0.15 # nyesuaiin sesuai dengan tingkat noise , biasanya 0 - 1 semakin kecil semakin cepat penyesuaiannya 
    if request.method == 'POST':
        save_path = os.path.join("", "audio.wav")
        request.files['audio_data'].save(save_path)
    
        with sr.AudioFile('audio.wav') as source:
            audio = r.record(source, offset=None)
            try:
                response = r.recognize_google(audio)
                print("Text: "+response)
            except Exception as e:
                print("Exception: "+str(e))
                
    return response

    

if __name__ == "__main__":
    app.run(debug=True)