from flask import Flask, render_template, request
import subprocess
import inspect
# from test_header import *
import os
import re


app = Flask(__name__)

directory = r'C:\Users\siddi\OneDrive\Desktop\UI-ORDERING-TEST-SUITES'

# Define a dictionary to store the methods under their respective service keys
services = {}

# Regular expression pattern to match method names starting with 'test_'
method_pattern = re.compile(r"def\s+test_(\w+)\s*\(")

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.py') and filename.startswith('test'):
        file_path = os.path.join(directory, filename)
        
        # Extract service key from the filename (without extension)
        service_key = os.path.splitext(filename)[0]
        
        # Initialize an empty list to store methods for this service
        service_methods = []
        
        # Open the file with proper encoding and search for method names
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = method_pattern.match(line)
                if match:
                    method_name = match.group(1)
                    service_methods.append(method_name)
        
        # Store the list of methods under the service key in the dictionary
        services[service_key] = service_methods

# Print the dictionary
print(services)

# # List to store docstrings of test functions
# test_docstrings = []

# # Get members of the module
# members = inspect.getmembers(test_header)

# # Iterate over members to find test functions and extract their docstrings
# for name, obj in members:
#     if inspect.isfunction(obj) and name.startswith('test_'):
#         docstring = inspect.getdoc(obj)
#         if docstring:
#             test_docstrings.append(docstring)

# # Print the list of docstrings
# for i, docstring in enumerate(test_docstrings, 1):
#     print(f"Docstring for test_{i}:")
#     print(docstring)
#     print()

@app.route('/')
def index():
    return render_template('index.html', services=services)

@app.route('/execute', methods=['POST'])
def execute_tests():
    try:
        selected_service = request.form['service']
        selected_test = request.form['test']
        # command = f"pytest -m {selected_test} --html=Report.html"
        test_file = os.path.join(directory, 'test_header.py::'+'test_'+selected_test)
        command = f"pytest {test_file} --html=Report.html"
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


