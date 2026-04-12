
from flask import Flask , jsonify
import requests
import datetime

# Creating the app
app = Flask(__name__)

# Using decorator to connect the URL to python
@app.route('/',methods=['GET'])
def home():
    return jsonify({"Message" : "Home page in API is running"}) # convert dic to json

@app.route('/status')
def status():
    return jsonify({"Version":"1.0.0","status":"healthy"})

@app.route('/hello_name/<name>')
def hello_name(name):
    return jsonify({"message": f"Hello {name}!"})

@app.route('/get_date')
def get_date():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")  
    return jsonify({"date": current_date})

@app.route('/get_time')
def get_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return jsonify({"time": current_time})

if __name__ == '__main__':
    app.run(debug=True,port=5000)