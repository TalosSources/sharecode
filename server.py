"""
Flask server for the web app.
Serves the web app and the API.
"""

from flask import Flask, render_template, request, jsonify
from pool_manager import build_object_struct, get_available_object, print_struct
import os

objects_path = 'objects'
object_struct = build_object_struct(objects_path)

app = Flask(__name__)

"""
Serves the web app.
"""
@app.route('/')
def index():
    return render_template('index.html')


"""
Serves the API. Client sends a POST request asking for an available object.
The server returns the object, or a time to wait before the first object becomes available.
"""
@app.route('/api', methods=['POST'])
def api():
    print_struct(object_struct)
    object_path, time_left = get_available_object(object_struct)
    if object_path is not None:
        #loads the file at object_path
        with open(os.path.join(objects_path, object_path), 'r') as object_file:
            object = object_file.read()
        #and then sends it as a response
        return jsonify({'object': object})
    elif time_left is not None:
        return jsonify({'time_left': time_left})
    else:
        #no object is available for today
        return jsonify({'error': 'No object available for today :('})

host = 'localhost'
port = 5000
if __name__ == '__main__':
    app.run(host=host, port=port)
