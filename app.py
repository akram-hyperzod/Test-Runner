from flask import Flask, render_template, request
import subprocess
import os


app = Flask(__name__)

services = {
    'Auth Service': ['loginmodule', 'registermodule'],
    'Cart Service': ['cartmodule', 'testing1','testing2','testing3']
}

@app.route('/')
def index():
    return render_template('index.html', services=services)

@app.route('/execute', methods=['POST'])
def execute_tests():
    try:
        selected_service = request.form['service']
        selected_test = request.form['test']
        command = f"pytest -m {selected_test} --html=Report.html"
        
        # Replace the print statement with actual command execution
        print("Executing command:", command)
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        return 'Test Executed Successfully.'
    except Exception as e:
        return f'Failed to execute test. Error: {str(e)}'
    

@app.route('/send_report', methods=['POST'])
def send_report():
    try:
        # Change directory to where send_slack.py is located
        os.chdir(r'C:\Users\siddi\OneDrive\Desktop\UI-ORDERING-TEST-SUITES')
        # Execute send_slack.py using subprocess
        subprocess.run([r'C:\Users\siddi\OneDrive\Desktop\UI-ORDERING-TEST-SUITES\venv\Scripts\python.exe', 'send_slack.py'])
        return 'Report sent successfully'
    except Exception as e:
        return f'Failed to send report. Error: {str(e)}'


if __name__ == '__main__':
    app.run(debug=True)


