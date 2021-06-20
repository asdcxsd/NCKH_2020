
from Application.Account import config_update_by_id, get_id_account
import json
import threading
from Application.Process_running import ProcessRunning
from urllib.parse import urlparse
from bson.objectid import ObjectId
from flask import Blueprint, Response, request
from api.v1.output import make_output
from Framework.Framework import Framework
from Application.run import Run
Main = Blueprint('Main', __name__)

# run all function
@Main.route('/status', methods=['GET'])
def run_status():
    try:
        _id = request.args['_id']
        proStatus = ProcessRunning("Status", update_db=False)
        proStatus.get_from_db(_id)
        dataResult = proStatus.to_json()
        return Response(make_output(data = dataResult, message ='success'), mimetype="application/json", status=200)
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)

@Main.route('/run', methods=['POST'])
def running():
    dataResult = {}
    try:
        if "input_raw_id" in request.form: 
            input_raw_id = request.form['input_raw_id']
            if "name" in request.form:
               name_run = request.form['name']
            else:
                name_run = "No Name"
            input_json_id = json.loads(input_raw_id)
            proRunning = ProcessRunning(name_run)
            def thread_run(proRunning, input_json_id):
                Run(proRunning, input_json_id )
            threading.Thread(target=thread_run, args=(proRunning, input_json_id, )).start()
            dataResult['_id'] = proRunning._id
        else: raise Exception("Target not exist!")
        return Response(make_output(data = dataResult, message ='success'), mimetype="application/json", status=200)
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)


@Main.route('/config', methods=['POST'])
def upload_config_api():
    try:
        data = request.form
        if "_id" in request.form: 
            data.pop('_id', None)
            _id = config_update_by_id(data, _id=request.form['_id'])
        else:
            _id = config_update_by_id(data)
        return Response(make_output(data = {"_id": _id}, message ='success'), mimetype="application/json", status=200)
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)



@Main.route('/login', methods=['POST'])
def login_account():
    
    try:

        username = request.form['username']
        password = request.form['password']
        _id = get_id_account(username, password)
        if _id == False:
            message = 'Login Fail'
            data = {
                "message" : "username or password wrong!!"
            }
        else:
            message = 'Login Success'
            data = {
                "_id" : _id
            }

        return Response(make_output(data = data, message =message), mimetype="application/json", status=200)
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)

