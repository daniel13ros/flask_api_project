from flask import Flask , request , jsonify
import datetime

app = Flask(__name__)

database = [
    {"id": 1, "name": "Daniel", "status": "Admin"},
    {"id": 2, "name": "System", "status": "Active"}
]

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
                padding: 30px;
                border-radius: 20px;
                backdrop-filter: blur(12px);
                box-shadow: 0 10px 40px rgba(0,0,0,0.4);
                width: 450px; 
            }}

            .scroll-box {{
                max-height: 300px; 
                overflow-y: auto;  
                margin-top: 20px;
                padding: 10px;
                background: rgba(0, 0, 0, 0.2);
                border-radius: 10px;
                text-align: left;
            }}

            .scroll-box::-webkit-scrollbar {{
                width: 8px;
            }}
            .scroll-box::-webkit-scrollbar-thumb {{
                background: #60a5fa;
                border-radius: 10px;
            }}

            .record-item {{
                background: rgba(255,255,255,0.05);
                margin-bottom: 8px;
                padding: 12px;
                border-radius: 8px;
                border-left: 4px solid #60a5fa;
                display: flex;
                justify-content: space-between;
                align-items: center;
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
        <a href="/get_data">View All Data</a>
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
    
# ---------------- GET ALL DATA ----------------
@app.route('/get_data')
def get_data():
    list_items = ""
    for item in database:
        list_items += f"""
        <div class="record-item">
            <div>
                <strong style="color: #60a5fa;">#{item.get('id')}</strong> 
                <span style="margin-left: 10px;">{item.get('name', 'N/A')}</span>
            </div>
            <small style="color: #94a3b8;">{item.get('status', 'Active')}</small>
        </div>
        """
    
    if not list_items:
        list_items = "<p style='text-align:center; color:#94a3b8;'>No records found...</p>"

    return wrap_html(f'''
        <h1>Database Content</h1>
        <p>Current records in memory:</p>
        <div class="scroll-box">
            {list_items}
        </div>
        <p style="font-size: 12px; color: #94a3b8; margin-top: 10px;">Scroll to see more</p>
    ''')
    


# ---------------- POST  ----------------
@app.route('/create', methods=['POST'])
def create_data():
    data = request.get_json()
    if not data:
        return "No data provided", 400
        
    new_id = len(database) + 1
    data['id'] = new_id
    database.append(data)
    
    return wrap_html(f'''
        <h1>Success!</h1>
        <p>Added <b>{data.get('name')}</b> to database.</p>
        <a href="/get_data">View Updated Data</a>
    '''), 201
# ---------------- PUT  ----------------
@app.route('/update/<int:id>', methods=['PUT'])
def update_data(id):
    data = request.get_json()
    
    return wrap_html(f'''
        <h1>PUT Success!</h1>
        <p>Updated record ID: <b>{id}</b></p>
        <pre>{data}</pre>
    ''')

# ---------------- DELETE  ----------------
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_data(id):
    return wrap_html(f'''
        <h1>DELETE Success!</h1>
        <p>Record ID <b>{id}</b> has been removed.</p>
    ''')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)