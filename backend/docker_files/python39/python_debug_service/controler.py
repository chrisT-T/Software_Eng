import os
import random
import shlex
import subprocess
import threading

import requests
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__, template_folder='.')
CORS(app, resources=r'/*')
socketio = SocketIO(app, cors_allowed_origins="*")

debug_service_input_server = {}
debug_service_input_client = {}
debug_service_output_server = {}
debug_service_output_client = {}
debug_service_port = {}


def forwarding_application_output(token: str):
    max_read_bytes = 1024 * 20
    while True:
        socketio.sleep(0.01)
        try:
            output = os.read(debug_service_output_client[token], max_read_bytes).decode()
            socketio.emit("debug_stdout", {"output": output, 'token': token})
        finally:
            pass


def create_service(token):
    '''
    create a new debug service in a new subprocess, then current thread blocked.
    When the service exit, emit a event "service_exit" by socket.io
    '''
    debug_service_input_server[token], debug_service_input_client[token] = os.pipe()
    debug_service_output_client[token], debug_service_output_server[token] = os.pipe()

    # start the output forwarding
    forwarding_thread = threading.Thread(target=forwarding_application_output, args=(token), daemon=True)
    forwarding_thread.run()

    port = random.randint(35000, 60000)
    while is_port_in_use(port):
        port = random.randint(35000, 60000)

    run_command = shlex(f"python /python_debug_service/app.py runserver {port}")
    subprocess.call(run_command, stdin=os.fdopen(debug_service_input_server[token], 'r'), stdout=os.fdopen(debug_service_output_server, 'w'))
    # service terminated, for any reason
    socketio.emit("service_exit", {'token': token})

    # kill the thread after 0.5s delay
    forwarding_thread.join(0.5)


'''
HTTP forwarding, from client to container(here) to debug service
'''


@app.route('/debugger/getstack', methods=['POST'])
def getStack():
    data = request.get_json()
    token: str = data['token']
    port: int = data['port']
    resp = requests.post(f'http://localhost:{port}/pdb/getstack', json={'token': token})
    return make_response(resp.text, resp.status_code)


@app.route('/debugger/getfunc', methods=['POST'])
def getFunc():
    data = request.get_json()
    token: str = data['token']
    port: int = data['port']
    resp = requests.post(f'http://localhost:{port}/pdb/getfunc', json={'token': token})
    return make_response(resp.text, resp.status_code)


@app.route('/debugger/runcmd', methods=['POST'])
def runcmd():
    data = request.get_json()
    token = data['token']
    cmd = data['cmd']
    port = data['port']
    resp = requests.post(f'http://localhost:{port}/pdb/runcmd', json={'token': token, 'cmd': cmd})
    return make_response(resp.json(), resp.status_code)


@app.route('/debugger/curframe', methods=['POST'])
def get_current_frame():
    data = request.get_json()
    token = data['token']
    port = data['port']
    resp = requests.post(f'http://localhost:{port}/pdb/curframe', json={'token': token})
    return make_response(resp.text, resp.status_code)


@app.route('/debugger/repr', methods=['POST'])
def get_repr():
    data = request.get_json()
    token = data['token']
    repr = data['repr']
    port = data['port']
    resp = requests.post(f'http://localhost:{port}/pdb/repr', json={'token': token, 'repr': repr})
    return make_response(resp.text, resp.status_code)


@app.route('/debugger/debug', methods=['POST'])
def http_start_debug():
    data = request.get_json()
    token = data['token']
    path = data['filepath']
    port = data['port']
    resp = requests.post(f'http://localhost:{port}/pdb/debug', json={'token': token, 'filepath': path})
    return make_response(resp.text, resp.status_code)


@socketio.on("debug_stdin")
def socket_debug_stdin(data):
    '''
    the standard input of the debugging app

    params: data['input']
    '''
    token = request.sid
    input_msg = data['input']
    os.write(debug_service_input_client[token], input_msg.encode())


@socketio.on("create_service")
def socket_create_service():
    token = request.sid
    create_service_thread = threading.Thread(target=create_service, args=(token), daemon=True)
    create_service_thread.start()


@socketio.on("connect")
def socket_connect():
    pass


def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


@app.cli.command("runserver")
def runserver():
    print("Set")
    app.run(port=30005, host="0.0.0.0")


if __name__ == '__main__':
    app.cli()
