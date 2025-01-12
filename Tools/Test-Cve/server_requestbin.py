from flask import Flask, request
import os, subprocess, datetime, time
from flask import jsonify
import json
import zipfile


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

@app.route('/checkupdatetool', methods=['POST'])
def check_tool_available_update_request(): 
    try: 
        if "list_tools" in request.form: 
            data = json.load(request.form['list_tools'])
            list_tool_check_update = data['data']
            list_tool_on_server = os.listdir(os.path.join(os.getcwd(), "Tool_Update_Folder"))
            list_update_client = [x.lower() for x in list_tool_check_update]
            list_update_server = [x.lower() for x in list_tool_on_server]
            result = []
            for tool_on_client in list_update_client: 
                toolname_client = tool_on_client.split('v')[0]
                version_client = tool_on_client.split('v')[1]
                check = [list_update_server.index(i) for i in list_update_server if toolname_client in i]
                if len(check) != 0: 
                    tool_on_server = list_update_server[check[0]]
                    version_server = tool_on_server.split('v')[1]
                    if version_server > version_client: 
                        result.append({tool_on_server, tool_on_client})
                        list_update_server.pop(tool_on_server)
            for i in list_update_server: 
                result.append({i,""})
            data = {
                "message": "success",
                "data": result
            }
            return jsonify(data)
    except Exception as e: 
        data = {
            "message": "fail", 
            "data": str(e) 
        }
        return jsonify(data)



@app.route("/listtoolupdate", methods=['GET'])
def list_tool_for_update(): 
    folder = os.path.join(os.getcwd(), "Tool_Update_Folder")
    files = os.listdir(folder)
    result = []
    for file in files: 
        filename = file.replace(".zip", "")
        temp = {}
        temp['toolname'] = filename.split('v')[0]
        temp['toolversion'] = filename.split('v')[1]
        temp['tool_filename'] = file
        result.append(temp)
    data_return = {
        "message": "success", 
        "data": result
    }
    return jsonify(data_return)


@app.route("/tool/download/<path:filename>", methods=['GET', 'POST'])
def download_tool(filename): 
    return send_from_directory(os.path.join(os.getcwd(), "Tool_Update_Folder"), filename=filename)
    


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)

