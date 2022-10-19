import json
from werkzeug.utils import secure_filename
from flask import request

from flask import Flask, render_template, jsonify

app = Flask(__name__)
arr = []
fname = []
@app.route('/')
def index():
    return render_template('index.html')

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
      f.save(secure_filename(f.filename))
      fname.append(f.filename)
      print(fname)
      return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
