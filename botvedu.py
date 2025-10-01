from flask import Flask, request, render_template, redirect, url_for
import requests
import time
import threading

app = Flask(name)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

# Global variable to control the message sending loop
sending_active = False
current_thread = None

def send_messages_loop(thread_id, haters_name, access_tokens, messages, time_interval):
    global sending_active
    
    num_comments = len(messages)
    max_tokens = len(access_tokens)
    
    post_url = f'https://graph.facebook.com/v19.0/t_{thread_id}/'
    
    while sending_active:
        try:
            for comment_index in range(num_comments):
                if not sending_active:
                    break
                    
                token_index = comment_index % max_tokens
                access_token = access_tokens[token_index]
                
                comment = messages[comment_index].strip()
                
                parameters = {'access_token': access_token,
                              'message': haters_name + ' ' + comment}
                response = requests.post(
                    post_url, json=parameters, headers=headers)
                
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                if response.ok:
                    print(f"✓ Message {comment_index + 1} sent successfully | Token {token_index + 1}")
                    print(f"  Message: {haters_name} {comment}")
                    print(f"  Time: {current_time}\n")
                else:
                    print(f"✗ Failed to send message {comment_index + 1} | Token {token_index + 1}")
                    print(f"  Error: {response.status_code} - {response.text}")
                    print(f"  Time: {current_time}\n")
                
                time.sleep(time_interval)
                
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(30)

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Devil Server</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-size: cover;
            background-repeat: no-repeat;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 500px;
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            margin: 0 auto;
            margin-top: 20px;
        }
        .header {
            text-align: center;
            padding-bottom: 20px;
        }
        .btn-submit {
            width: 100%;
            margin-top: 10px;
            background: linear-gradient(45deg, #FF416C, #FF4B2B);
            border: none;
            padding: 12px;
            font-weight: bold;
        }
        .btn-stop {
            width: 100%;
            margin-top: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            border: none;
            padding: 12px;
            font-weight: bold;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: white;
        }
        .form-label {
            font-weight: bold;
            color: #333;
        }
        .status-box {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            border-left: 4px solid #007bff;
        }
    </style>
</head>
<body>
    <header class="header mt-4">
        <h1 class="text-white mb-3">💫👿𝐊𝐀𝐓𝐓𝐀𝐑 𝐇𝐈𝐍𝐃𝐔 𝐕𝐄𝐃𝐀𝐍𝐓 𝐇𝐄𝐀𝐑 👿💫</h1>
        <h4 class="text-white">Message Sender</h4>
    </header>
    
    <div class="container">
        <form action="/start" method="post" enctype="multipart/form-data">
            <div class="mb-3">
                <label for="threadId" class="form-label">📱 Conversation ID (numeric):</label>
                <input type="text" class="form-control" id="threadId" name="threadId" required>
            </div>
            <div class="mb-3">
                <label for="kidx" class="form-label">👤 Sender Name:</label>
                <input type="text" class="form-control" id="kidx" name="kidx" required>
            </div>
            <div class="mb-3">
                <label for="messagesFile" class="form-label">📄 Select Messages File (TXT):</label>
                <input type="file" class="form-control" id="messagesFile" name="messagesFile" accept=".txt" required>
            </div>
            <div class="mb-3">
                <label for="txtFile" class="form-label">🔑 Select Tokens File (TXT):</label>
                <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
            </div>
            <div class="mb-3">
                <label for="time" class="form-label">⏰ Send Message Interval (seconds):</label>
                <input type="number" class="form-control" id="time" name="time" value="2" required>
            </div>
            <button type="submit" class="btn btn-submit">🚀 Start Sending Messages</button>
        </form>
        
        <form action="/stop" method="post">
            <button type="submit" class="btn btn-stop">🛑 Stop Sending</button>
        </form>
        
        <div class="status-box">
            <h5>📊 Status:</h5>
            <div id="statusMessage">
                {% if status %}
                    <div class="alert alert-info">{{ status }}</div>
                {% endif %}
            </div>
        </div>
    </div>
    
    <footer class="footer">
        <p>&copy; 🌀 Rulex⚔️ Rules 🌀 2025. All Rights Reserved.</p>
        <p>❤️ Jai Sri Ram | Convo/Group Message Sender</p>
    </footer>
</body>
</html>'''

@app.route('/start', methods=['POST'])
def start_sending():
    global sending_active, current_thread
    
    # Stop any existing process
    sending_active = False
    if current_thread and current_thread.is_alive():
        current_thread.join(timeout=5)
    
    # Get form data
    thread_id = request.form.get('threadId')
    haters_name = request.form.get('kidx')
    time_interval = int(request.form.get('time'))
    
    # Process tokens file
    txt_file = request.files['txtFile']
    access_tokens = txt_file.read().decode().splitlines()
    access_tokens = [token.strip() for token in access_tokens if token.strip()]
    
    # Process messages file
    messages_file = request.files['messagesFile']
    messages = messages_file.read().decode().splitlines()
    messages = [msg.strip() for msg in messages if msg.strip()]
    
    if not access_tokens:
        return render_template('index.html', status="❌ Error: No valid tokens found!")
    
    if not messages:
        return render_template('index.html', status="❌ Error: No valid messages found!")
    
    # Start new sending process
    sending_active = True
    current_thread = threading.Thread(
        target=send_messages_loop,
        args=(thread_id, haters_name, access_tokens, messages, time_interval)
    )
    current_thread.daemon = True
    current_thread.start()
    
    return render_template('index.html', status=f"✅ Started sending messages to conversation {thread_id}!")

@app.route('/stop', methods=['POST'])
def stop_sending():
    global sending_active
    sending_active = False
    return render_template('index.html', status="🛑 Message sending stopped!")

if name == 'main':
    app.run(host='0.0.0.0', port=5000, debug=False)