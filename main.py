from flask import Flask, render_template, request
import speech_recognition as sr
import os
from scipy.io import wavfile
import wavio as wv

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

        wa = wv.read("audio.wav")
        wv.write("audio_output.wav", wa.data, wa.rate,sampwidth=wa.sampwidth)
        
        freq_sample, sig_audio = wavfile.read("audio_output.wav")

        print('\nShape of Signal:', sig_audio.shape)
        print('Signal Datatype:', sig_audio.dtype)
        print('Signal duration:', round(sig_audio.shape[0] / float(freq_sample), 2), 'seconds')
        print(len(sig_audio))

        add_response = "<br> Shape of Signal : " + str(sig_audio.shape) + "<br> Signal Datatype : " + str(sig_audio.dtype) + "<br> Signal duration : " + str(round(sig_audio.shape[0] / float(freq_sample), 2)) +  'seconds'

        with sr.AudioFile('audio_output.wav') as source:
            audio = r.record(source, offset=None)
            try:
                response = r.recognize_google(audio)
                print("Text: "+response)
                final_response = str(response) + str(add_response)
            except Exception as e:
                print("Exception: "+str(e))
                
    return final_response

if __name__ == "__main__":
    app.run(debug=True)