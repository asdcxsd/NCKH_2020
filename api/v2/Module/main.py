
from Application.Account import config_update_by_id, delete_config_with_id, get_id_account, get_config_query
import json
from Application.Function.Connect_Database import get_all_process, get_recon, get_exploit_cve, get_input, get_shell_log_data
from bson.json_util import dumps
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


@Main.route("/getlistmodule", methods=['GET'])
def get_list_module(): 
    try: 
        framework = Framework()
        Listmodule = framework.get_list_of_module()
        data = []
        for module in Listmodule:
            data.append(framework.get_info_main_module(module))
        return Response(make_output(data=data, message="success"), mimetype="application/json", status=200)
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)


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

@Main.route('/getallstatus', methods=['GET'])
def get_all_status_request(): 
    try: 
        status, data = get_all_process()
        if status: 
            result = []
            for cur in data: 
                temp = json.loads(dumps(cur))
                temp['_id'] = temp['_id']['$oid']
                result.append(temp)
            return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
        else: 
            raise Exception('Can not get data')
    except Exception as e: 
        return Response(make_output(message="fail", data=str(e)), mimetype="application/json", status=404)

@Main.route('/getallstatusrunning', methods=['GET'])
def get_all_status_running_request(): 
    try: 
        status, data = get_all_process()
        if status: 
            result = []
            for cur in data: 
                each_data = {}
                temp = json.loads(dumps(cur))
                each_data['_id'] = temp['_id']['$oid']
                each_data['Status'] = temp['Status']
                result.append(each_data)
            return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
        else: 
            raise Exception('Can not get data')
    except Exception as e: 
        return Response(make_output(message="fail", data=str(e)), mimetype="application/json", status=404)



@Main.route('/getmoduleprocess', methods=['POST'])
def get_module_of_process(): 
    try: 
        result = []
        if "process_id" in request.form: 
            query = {
                "_id_process": request.form['process_id']
            }
        status, data = get_recon(query)
        if status and data.count() > 0: 
            result.append("Module_Reconnaissance")
        status, data = get_exploit_cve(query)
        if status and data.count() > 0: 
            result.append("Module_Exploit")
        status,data = get_input(query)
        if status and data.count() > 0: 
            result.append("Module_Input")
        status, data = get_shell_log_data(query)
        if status and data.count() > 0: 
            result.append("Module_Output")
        return Response(make_output(data=result, message='success'), mimetype="application/json", status=200)
    except Exception as e: 
        return Response(make_output(data=str(e), message='fail'), mimetype="application/json", status=404)
#Hàm chạy tất cả các module còn lại
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
        if "Cf_Account_id" in request.form: 
            _id = config_update_by_id(data, _id=request.form['Cf_Account_id'])
        else:
            _id = config_update_by_id(data)
        return Response(make_output(data = _id, message ='success'), mimetype="application/json", status=200)
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)

@Main.route("/getallconfig", methods=['GET'])
def get_list_config(): 
    try: 
        status, ListConfig = get_config_query({})
        if status: 
            result = []
            data = json.loads(dumps(ListConfig))
            for config in data: 
                config['_id'] = str(config['_id'])
                result.append(config)
        return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)

@Main.route("/getconfig", methods=['POST'])
def get_config(): 
    try: 
        query = {}
        if "config_id" in request.form: 
            query['_id'] = ObjectId(request.form['config_id'])
            [status, data] = get_config_query(query)
            if status: 
                result = json.loads(dumps(data[0]))
                result['_id'] = str(result['_id'])
                return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
            else: raise Exception(str(data))
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)


@Main.route("/deleteconfig", methods=['DELETE'])
def delete_config(): 
    try: 
        data_remove = {}
        if "config_id" in request.form: 
            data_remove['_id'] = ObjectId(request.form['config_id'])
            [status, data] = get_config_query(data_remove)
            if status == False: raise Exception(str(data))
            if data.count() > 0: 
                status = delete_config_with_id(data_remove)
                if status == True: 
                    return Response(make_output(data="delete config success", message="success"), mimetype="application/json", status=200)
                else: 
                    raise Exception("Can not delete config")
            else: 
                raise Exception("Config not exists")
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)

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

@Main.route('/getaccountconfig', methods=['POST'])
def get_account_config():
    try: 
        account_id = request.form['account_id']
        query = {
            "Cf_Account_id": account_id
        }
        status,data = get_config_query(query)
        if data.count() > 0: 
            result = json.loads(dumps(data[0]))
            data = result["_id"]
            return Response(make_output(message="success", data=data), mimetype="application/json", status=200)
        else: 
            raise Exception("Config not exists")
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)
