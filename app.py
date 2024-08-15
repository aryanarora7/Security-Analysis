from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO
import subprocess

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# List of valid usernames and passwords
valid_users = {
    'admin': 'password123',
    'user1': 'pass456'
}

# Initialize session data
app.config['MAX_ATTEMPTS'] = 3

@app.route('/')
def index():
    # Reset the wrong attempt count
    session['wrong_attempts'] = 0
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in valid_users and valid_users[username] == password:
        # Correct credentials, grant access
        session['logged_in'] = True
        return redirect(url_for('access_granted'))  # Redirect to access_granted.html
    else:
        # Incorrect credentials, increment wrong attempt count
        session['wrong_attempts'] = session.get('wrong_attempts', 0) + 1

        # Check if maximum attempts reached
        if session['wrong_attempts'] >= app.config['MAX_ATTEMPTS']:
            # Capture image on maximum attempts
            capture_image()

        return render_template('login.html', error='Invalid username or password')

@app.route('/access_granted')
def access_granted():
    if session.get('logged_in'):
        return render_template('access_granted.html')
    else:
        return redirect(url_for('index'))  # Redirect to login page if not logged in

# Function to capture image (to be replaced with actual image capture logic)
def capture_image():
    try:
        subprocess.run(['ffmpeg', '-f', 'dshow', '-i', 'video="USB2.0 HD UVC WebCam"', '-vframes', '1', 'static/webcam98.jpg'], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error capturing image: {e}')

if __name__ == '__main__':
    socketio.run(app, debug=True)
