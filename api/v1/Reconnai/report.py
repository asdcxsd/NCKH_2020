
import os
from api.v1.uploadfile import allowed_file
from api.v1.output import make_output
from datetime import datetime
from bson.objectid import ObjectId
from flask import Blueprint, Response, request
from configvalue import  PUBLIC_FOLDER as UPLOAD_FOLDER , ALLOWED_EXTENSIONS
UPLOAD_FOLDER_REPORT = UPLOAD_FOLDER + "REPORTS/"
Report = Blueprint('report', __name__)
import xml.etree.ElementTree as ET

@Report.route('/uploadReport', methods=['POST'])
def request_post_report():
	# check if the post request has the file part
    if 'file' not in request.files or 'target_id' not in request.form:
        return Response(make_output(message =  "fail", data= "No file part in the request"), mimetype="application/json", status=404)

    file = request.files['file']
    target_id = request.form['target_id']
    if file.filename == '':
        return Response(make_output(message =  "fail", data= "No file selected for uploading"), mimetype="application/json", status=404)


    if file and allowed_file(file.filename):
        ts = str(int(datetime.now().timestamp()))
        filename =  "Acunetix-" + target_id + "-" + ts + "-"+ file.filename
        file.save(os.path.join(UPLOAD_FOLDER_REPORT, filename))
        return Response(make_output(message =  "success", data= "File successfully uploaded"), mimetype="application/json", status=200)

    else:
        return Response(make_output(message =  "fail", data= "Allowed file types are html zip"), mimetype="application/json", status=404)



@Report.route('/getReports', methods=['GET'])
def request_get_report():
	# check if the post request has the file part
    if 'target_id' not in request.args:
        return Response(make_output(message =  "fail", data= "No file part in the request"), mimetype="application/json", status=404)

    target_id = request.args['target_id']
    ans = []
    for path, subdirs, files in os.walk(UPLOAD_FOLDER_REPORT):
        for file in files:
            namesplit = file.split('-', 3)
            if namesplit[1] != target_id:continue
            ts = int(namesplit[2])
            time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            file_stats = os.stat(path +  file)
            size = round(1.0 * file_stats.st_size / 1024 , 3)
            data = {
                "Report" : namesplit[0],
                "Target_id" : namesplit[1],
                "DateUpload" : time,
                "NameFile" : file,
                "SizeFile" : size
            }
            ans.append(data)

    return Response(make_output(message =  "success", data=ans), mimetype="application/json", status=200)


