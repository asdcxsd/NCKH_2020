from flask import Flask, request
import os, subprocess, datetime, time

from flask.helpers import send_from_directory
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

@app.route('/cve/download/<path:filename>', methods=['GET', "POST"])
def download(filename): 
    return send_from_directory(os.path.join(os.getcwd(), "CVE_Folder"), filename=filename)


@app.route('/upload', methods=['POST'])
def upload_file_request(): 
    try: 
        file = request.files['file_upload']
        folder = os.path.join(os.getcwd(), "CVE_Folder")
        file.save(os.path.join(folder, file.filename))
        return "upload file thanh cong"

    except Exception as e: 
        print(str(e))
        return str(e)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)

