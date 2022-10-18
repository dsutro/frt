import json

from flask import request

from flask import Flask, render_template

app = Flask(__name__)
arr = []
@app.route('/')
def index():
    return render_template('index_1.html')

@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary
    print((result['firstname'])) # Printing the new dictionary
    arr.append(result['firstname'])
    return result

if __name__ == '__main__':
    app.run(debug=True)
