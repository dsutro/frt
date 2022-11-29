import os
import shutil
import json
from werkzeug.utils import secure_filename
from flask import request
from main import run_ga
from main import create_spectrogram

from flask import Flask, render_template, jsonify

app = Flask(__name__)
arr = []
fname = "file_"
@app.route('/')
def index():
    os.makedirs(os.path.join(app.instance_path, 'mp3files'), exist_ok=True)
    params = {
        "harmonicity" : 3.5 ,
        "modulationIndex" : 25 ,
        "detune" : 0 ,
        "car_type" : "sine" ,
        "amp_attack" : 0.01 ,
        "amp_decay" : 0.01 ,
        "amp_sustain" : 1 ,
        "amp_release" : 5 ,
        "mod_type" : "sine" ,
        "mod_attack" : 0.01 ,
        "mod_decay" : 0 ,
        "mod_sustain" : 1 ,
        "mod_release" : 10
        # "attack": 0.01, 
        # "release": 10
        # "attack":0.01,
        # "release":1000
        }
    return render_template('index.html',params=params)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      file_number = open("file_count", "r+")
      num = file_number.read()
      num = int(num)
      file_number.seek(0)
      file_number.write(str(num+1))
      file_number.close()
      fname = "file_{}.wav".format(num)
      f.save(os.path.join('static', 'mp3files', secure_filename(fname)))
      pth = "static/mp3files/" + fname
      shutil.copy(pth,'static/mp3files/file_0.mp3')
      source_sound = pth
      #print(pth)
      create_spectrogram(pth, True)
      final_dict = run_ga(pth)

      #print(final_dict)
      backendHarmonicity = final_dict["modulator"]/final_dict["carrier"]
      params = {
        "harmonicity" : backendHarmonicity ,
        "modulationIndex" : final_dict["index"] ,
        "detune" : 0 ,
        "car_type" : "sine" ,
        "amp_attack" : final_dict["attack"] ,
        "amp_decay" : 0.01 ,
        "amp_sustain" : 1 ,
        "amp_release" : final_dict["release"] ,
        "mod_type" : "sine" ,
        "mod_attack" : final_dict["attack"] ,
        "mod_decay" : 0 ,
        "mod_sustain" : 1 ,
        "mod_release" : final_dict["release"] ,
        "individual" : final_dict["individual"]
      }
      resynthesized_sound = "../tmp/temp_audio_gen_9_" + str(params["individual"]) + ".wav"

      create_spectrogram(resynthesized_sound, False)

      return render_template("index.html",params=params)

if __name__ == '__main__':
    app.run(debug=True)
