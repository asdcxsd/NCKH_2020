from flask import Flask, request
import os, subprocess, datetime, time
app = Flask(__name__)
FORMATTIME = "%d/%m/%YT%H:%M:%S"

@app.route('/')
def index():
    return "<h1>Hello, World!</h1></br> Version: 1.0 "

@app.route('/requestbin')
def requestbin():
    cmd = request.args.get('data')
    date_now = datetime.datetime.now()
    date_create = date_now.strftime(FORMATTIME)
    data = date_create + "   " + request.host_url + "   *" + cmd + "*\n"
    open("logfile.txt", 'a').write(data)
    return "OK"

@app.route('/logrequestbin')
def logrequestbin():
    data = "*" + request.args.get('data') + "*"
    time_start = datetime.datetime.now() 
    while (datetime.datetime.now() - time_start < datetime.timedelta(seconds=2)):

        time.sleep(1)
    in_data = open("logfile.txt", 'r').read()
    if data in in_data:
        return '{"status":"StatusSuccess"}'
    else:
        return '{"status":"Not Found"}'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)

