
from flask import Flask , jsonify
import requests
import datetime

# Creating the app
app = Flask(__name__)

def wrap_html(content):
    return f"""
    <html>
        <body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
            <div style="border: 1px solid #ddd; display: inline-block; padding: 20px; border-radius: 10px;">
                {content}
            </div>
            <br><br>
            <a href="/">Go Home</a>
        </body>
    </html>
    """

# Using decorator to connect the URL to python
@app.route('/',methods=['GET'])
def home():
    return wrap_html('<h1>Home Page</h1><p>API is running!</p><p><a href="/status">Check Status</a><br><a href="/hello_name/John">Say Hello to John</a><br><a href="/get_time">Get Current Time</a>')

@app.route('/status' , methods=['GET'])
def status():
    return wrap_html('<h1>Status</h1><p>API is healthy!</p>')

@app.route('/hello_name/<name>' , methods=['GET'])
def hello_name(name):
    return wrap_html(f'<h1>Hello {name}!</h1>')
def get_date():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")  
    return wrap_html(f'<h1>Current Date</h1><p>{current_date}</p>')

@app.route('/get_time')
def get_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return f"""
    <html>
        <head><meta http-equiv="refresh" content="1"></head>
        <body style="text-align: center; font-family: sans-serif;">
            <h1>Current Time </h1>
            <h1 style="font-size: 50px;">{current_time}</h1>
            <a href="/">Go Home</a>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True,port=5000)