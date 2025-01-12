import os
import urllib.request

from flask.wrappers import Request
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from flask import Blueprint, Response, request
from configvalue import  PUBLIC_FOLDER as UPLOAD_FOLDER , ALLOWED_EXTENSIONS
from api.v1.output import make_output
Upload = Blueprint('Upload', __name__)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@Upload.route('/fileupload', methods=['POST'])
def upload_file():
   
	# check if the post request has the file part
    if 'file' not in request.files or 'target_id' not in request.form:
        return Response(make_output(message =  "fail", data= "No file part in the request"), mimetype="application/json", status=404)

    file = request.files['file']
    target_id = request.form['target_id']
    if file.filename == '':
        return Response(make_output(message =  "fail", data= "No file selected for uploading"), mimetype="application/json", status=404)


    if file and allowed_file(file.filename):
        filename =  (file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return Response(make_output(message =  "success", data= "File successfully uploaded"), mimetype="application/json", status=200)

    else:
        return Response(make_output(message =  "fail", data= "Allowed file types are html zip"), mimetype="application/json", status=404)


