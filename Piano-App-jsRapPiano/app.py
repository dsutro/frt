import os
import json
from werkzeug.utils import secure_filename
from flask import request

from flask import Flask, render_template, jsonify

app = Flask(__name__)
arr = []
fname = "file_"
@app.route('/')
def index():
    os.makedirs(os.path.join(app.instance_path, 'mp3files'), exist_ok=True)
    params = {"attack":.05,"release":1000}
    return render_template('index.html',params=params)

@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary
    print((result['data'])) # Printing the new dictionarys
    arr.append(result['data'])
    return result

def send_sound(i):
    x = 2 ** ((i - 69) / 12)
    return str(x)

@app.route('/sound_feed')
def sound_feed():
    d = {'sound':send_sound(arr[-1])}
    print(fname, d)
    return jsonify(d)

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
      fname = "file_{}.mp3".format(num)
      f.save(os.path.join(app.instance_path, 'mp3files', secure_filename(fname)))
      print(fname)
      params = {"attack": 0.01, "release": 10}
      return render_template("index.html",params=params)

if __name__ == '__main__':
    app.run(debug=True)
