import os
import subprocess
from flask import Flask, send_from_directory

# Check if Flask is installed, and install it if not
try:
    from flask import Flask
except ImportError:
    print("Flask is not installed. You can install it with: pip3 install flask")
    exit(1)

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), './')

# Serving the index file
@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    if os.path.exists("app.py"):
        # If app.py exists, run it and return the output
        out = subprocess.Popen(['python3', 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        if out.returncode == 0:
            return stdout
        else:
            return f"<pre style='color: red;'>{stdout.decode('utf-8')}</pre>"
    
    if os.path.exists("index.html"):
        return send_from_directory(static_file_dir, 'index.html')
    else:
        return """
            <h1 align='center'>404</h1>
            <h2 align='center'>Missing index.html file</h2>
            <p align='center'><img src='https://github.com/4GeeksAcademy/html-hello/blob/main/.vscode/rigo-baby.jpeg?raw=true' /></p>
        """

# Serving any other image or file
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    full_path = os.path.join(static_file_dir, path)
    if not os.path.isfile(full_path):
        # If the path is a directory, serve its index.html if it exists
        index_html_path = os.path.join(full_path, 'index.html')
        if os.path.exists(index_html_path):
            return send_from_directory(static_file_dir, os.path.join(path, 'index.html'))
        return "Not Found", 404

    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # Avoid caching
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True, extra_files=['./'])
