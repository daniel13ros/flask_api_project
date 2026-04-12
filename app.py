from flask import Flask , jsonify

# Creating the app
app = Flask(__name__)

# Using decorator to connect the URL to python
@app.route('/',methods=['GET'])
def home():
    return jsonify({"Message" : "Pokemon API is running"}) # convert dic to json

@app.route('/status')
def status():
    return jsonify({"Version":"1.0.0","status":"healthy"})

@app.route('/hello_name/<name>')
def hello_name(name):
    return jsonify({"message": f"Hello {name}!"})

if __name__ == '__main__':
    app.run(debug=True,port=5000)