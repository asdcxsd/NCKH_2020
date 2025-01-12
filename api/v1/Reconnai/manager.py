

from Library.Reconnai.manager_tools import import_tool_reconnai, load_tool_import, remove_tool_reconnai
import os
from api.v1.uploadfile import allowed_file
from datetime import datetime
from configvalue import  UPLOAD_FOLDER_TOOLS , ALLOWED_EXTENSIONS
from flask import Blueprint, Response, request
from api.v1.output import make_output
from bson.objectid import ObjectId
from threading import Thread
from Library.Reconnai.reconnaissance import Reconnaissance
from Library.Target.target import get_target_url
ManagerRecon = Blueprint('managerecon', __name__)
import xml.etree.ElementTree as ET

@ManagerRecon.route('/extension', methods=['GET'])
def request_get_extension_reconnaissance():
    try:
        if "type" in request.args:
            request_type = request.args['type']
        else: request_type = "offline"
        Recon = Reconnaissance()
        result = Recon.get_all_extension()
        ans = []
        for fo in result:
            func = fo.reconnaissance()
            info = func.info()
            if (info['type'] == request_type or request_type == "online") and info['type'] != 'internal':
                ans.append(info)

        return Response(make_output(data = ans, message ='success'), mimetype="application/json", status=200)
    except Exception as e:
        return Response(make_output(message =  "fail", data= "No data" ), mimetype="application/json", status=404)




@ManagerRecon.route('/uploadtool', methods=['POST'])
def upload_tool():
    try:
        # check if the post request has the file part
        if 'filename' not in request.form:
            return Response(make_output(message =  "fail", data= "No file part in the request"), mimetype="application/json", status=404)
        else:
            filename = request.form['filename']
        import_tool_reconnai(filename);
        return Response(make_output(message =  "success", data= "Tools successfully import"), mimetype="application/json", status=200)
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e)), mimetype="application/json", status=404)

@ManagerRecon.route('/deletetool', methods=['DELETE'])
def delete_tool():
    try:
        # check if the post request has the file part
        if 'filename' not in request.form:
            return Response(make_output(message =  "fail", data= "No file part in the request"), mimetype="application/json", status=404)
        else:
            filename = request.form['filename']
        remove_tool_reconnai(filename);
        return Response(make_output(message =  "success", data= "Tools successfully remove"), mimetype="application/json", status=200)
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e)), mimetype="application/json", status=404)


@ManagerRecon.route('/loadtool', methods=['GET'])
def load_tool():
    try:
       
        ans = load_tool_import();
        return Response(make_output(message =  "success", data= ans), mimetype="application/json", status=200)
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e)), mimetype="application/json", status=404)

load_tool_import