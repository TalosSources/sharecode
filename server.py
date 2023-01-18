"""
Flask server for the web app.
Serves the web app and the API.
"""

from flask import Flask, render_template, request, jsonify
from flask import send_from_directory
from pool_manager import build_object_struct, get_status, use_object, print_struct
import os
from flask_cors import CORS


objects_path = 'objects'
object_struct = build_object_struct(objects_path)

app = Flask(__name__)
CORS(app)

"""
Serves the web app.
"""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/objects/<path:path>')
def send_images(path):
    return send_from_directory('objects', path)


"""
Serves the API. Client sends a POST request asking for an available object.
The server returns the object, or a time to wait before the first object becomes available.
"""
@app.route('/getObject', methods=['GET', 'POST'])
def getObject():
    print_struct(object_struct)
    object_name, time_left = get_status(object_struct)
    if object_name is not None:
        #loads the file at object_path
        use_object(object_struct, object_name)
        #and then sends it as a response
        #if the object path ends with .png, we send its path instead of its content
        object_path = os.path.join(objects_path, object_name)
        if(object_name.endswith('.png')):
            return jsonify({'status': 'available', 'object': f"/{object_path}", 'type' : 'image'})
        else:
            with open(object_path, 'r') as object_file:
                object = object_file.read()
            return jsonify({'status': 'available', 'object': object, 'type' : 'string'})
    elif time_left is not None:
        return jsonify({'status' : 'waiting', 'time_left': time_left})
    else:
        #no object is available for today
        return jsonify({'status': 'unavailable'})

@app.route('/getStatus', methods=['GET','POST'])
def getStatus():
    print_struct(object_struct)
    object_path, time_left = get_status(object_struct)
    if object_path is not None:
        return jsonify({'status': 'available'})
    elif time_left is not None:
        return jsonify({'status': 'waiting', 'time_left': time_left})
    else:
        return jsonify({'status': 'unavailable'})

local_host = 'localhost'
lan_host = '146.169.148.56'
port = 5000
if __name__ == '__main__':
    app.run(host=lan_host, port=port)

