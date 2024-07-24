from flask import Flask, jsonify, request, send_from_directory
import subprocess
import os
import threading

app = Flask(__name__)
script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'auto_run.py'))
status = {"running": False, "output": ""}

def run_script():
    global status
    status["running"] = True
    process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    status["output"] = output.decode() + "\n" + error.decode()
    status["running"] = False

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/run-automation', methods=['POST'])
def run_automation():
    if status["running"]:
        return jsonify({"message": "Automation script is already running."}), 400

    thread = threading.Thread(target=run_script)
    thread.start()
    return jsonify({"message": "Automation script started."}), 200

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(status), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
