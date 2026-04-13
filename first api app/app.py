from flask import Flask
import datetime

app = Flask(__name__)

def wrap_html(content):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="1">
        <title>API</title>

        <style>
            body {{
                margin: 0;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #0f172a, #1e293b);
                color: white;
            }}

            .card {{
                text-align: center;
                background: rgba(255,255,255,0.08);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(12px);
                box-shadow: 0 10px 40px rgba(0,0,0,0.4);
                min-width: 300px;
            }}

            a {{
                display: block;
                margin-top: 10px;
                color: #60a5fa;
                text-decoration: none;
            }}

            a:hover {{
                color: #93c5fd;
            }}
        </style>
    </head>

    <body>
        <div class="card">
            {content}
            <a href="/">Go Home</a>
        </div>
    </body>
    </html>
    """

# ---------------- HOME ----------------
@app.route('/')
def home():
    return wrap_html("""
        <h1>Home Page</h1>
        <p>API is running!</p>

        <a href="/status">Check Status</a>
        <a href="/hello_name/Daniel">Say Hello</a>
        <a href="/get_time">Get Time</a>
        <a href="/get_date">Get Date</a>
    """)

# ---------------- STATUS ----------------
@app.route('/status')
def status():
    return wrap_html(f'''
                     <h1>Status</h1>
                     <p>API is healthy!</p>
                     '''
                     )

# ---------------- HELLO ----------------
@app.route('/hello_name/<name>')
def hello_name(name):
    return wrap_html(f'''
                     <h1>Hello {name}!</h1>
                     '''
                     )

# ---------------- DATE ----------------
@app.route('/get_date')
def get_date():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return wrap_html(f'''
                     <h1>Current Date</h1>
                     <p>{current_date}</p>
                     '''
                     )

# ---------------- TIME ----------------
@app.route('/get_time')
def get_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return wrap_html(f'''
                     <h1>Current Time</h1>
                     <p style='font-size:40px'>{current_time}</p>
                     '''
                     )

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)