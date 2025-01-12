from flask import Flask, render_template, request, session, jsonify, redirect, url_for,escape, Blueprint
from functools import wraps

from flask.wrappers import Response
Start = Blueprint('Start', __name__, template_folder='templates')
from .. import const
import requests
import  json


def GetConfigData(): 
    if session['config_id'] != '': 
        return [True, session['config_id']]
    else: 
        return [False, "Chưa cấu hình config"]
def login_required(func): 
    @wraps(func)
    def wrapper(*args, **kwargs): 
        if not "logged_in" in session: 
            return redirect(url_for('Login.login'))
        elif not session['logged_in']: 
            return redirect(url_for('Login.login'))
        else: 
            return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@Start.route('/start', methods=['GET'])
@login_required
def start(): 
    return render_template('start.html')

@Start.route('/getshelllog', methods=['POST'])
@login_required
def get_shell_log_request(): 
    if "process_id" in request.form: 
        processid = request.form['process_id']
    param = {
        "id_process": processid
    }
    res = requests.post(const.PUBLIC_API + "/api/v2/shell/getshelllogdata", data = param)
    return res.json()

@Start.route('/getconfigdata', methods=['GET'])
@login_required
def get_config_data(): 
    status, data = GetConfigData(); 
    result = {
        "data": data, 
        "message": status
    }
    return result

@Start.route('/getallstatus', methods=['GET'])
@login_required
def get_all_status_data():
    res = requests.get(const.PUBLIC_API + "/api/v2/module/getallstatus")
    return res.json()

@Start.route('/getallstatusrunning', methods=['GET'])
@login_required
def get_all_status_running_data():
    res = requests.get(const.PUBLIC_API + "/api/v2/module/getallstatusrunning")
    temp = json.dumps(res.json())
    return_data = 'data:%s\n\n' % temp
    headers = {
        "Content-Type": "text/event-stream; charset=utf-8"
    }
    return return_data, 200, headers

@Start.route('/getmoduleprocessrun', methods=['POST'])
@login_required
def get_module_of_process_request(): 
    param = {
        "process_id": request.form['process_id']
    }
    res = requests.post(const.PUBLIC_API + "/api/v2/module/getmoduleprocess", data=param)
    return res.json()

@Start.route("/getdashboard", methods=['GET'])
@login_required
def get_dashboard_info(): 
    res = requests.get(const.PUBLIC_API + "/api/v2/module/dashboardinfo")
    return res.json()

@Start.route("/getprocessdashboard", methods=['GET'])
@login_required
def get_process_dashboard_info(): 
    res = requests.get(const.PUBLIC_API + "/api/v2/module/processdashboard")
    result = res.json()
    process_count = [0]*12
    for key in result['data'].keys(): 
        i = int(key.split("/")[0])-1
        process_count[i] = result["data"][key]
    data_for_return = {
            "message": "success", 
            "data": process_count
        }
    return jsonify(data_for_return)

@Start.route("/getpocinfo", methods=['GET'])
@login_required
def get_poc_info_dashboard(): 
    res = requests.get(const.PUBLIC_API + "/api/v2/managepoc/pocdashboard")
    result = res.json()
    labels = []
    data = []
    for key in result['data'].keys(): 
        if key not in labels: 
            labels.append(key)
            data.append(result['data'][key])
    data_for_return = {
            "message": "success", 
            "labels": labels, 
            "data": data
        }
    return jsonify(data_for_return)      


@Start.route("/deleteprocess", methods=['POST'])
@login_required
def delete_process(): 
    if "process_id" in request.form: 
        process_id = request.form['process_id']
        param = {
            "process_id": process_id
        }
        res = requests.delete(const.PUBLIC_API + "/api/v2/module/delete", data = param)
        return res.json()

@Start.route("/stopprocess", methods=['POST'])
@login_required
def stop_process_request(): 
    if "process_id" in request.form: 
        process_id = request.form['process_id']
        data = {
            "_id": process_id
        }
        res = requests.post(const.PUBLIC_API + "/api/v2/module/stop", data = data)
        return res.json()
        

@Start.route('/run', methods=['POST'])
@login_required
def run_module(): 
    raw_id = {}
    raw_id['Input'] = []
    config_module = {}
    config_module['module'] = "ConfigSetup"
    config_module["_id"] = session['config_id']
    raw_id['Input'].append(config_module)
    if ("Target" in request.form) and(request.form['Target'] != ""): 
        target_module = {}
        target_module['module'] = "Target"
        target_module['_id'] = request.form['Target']
        raw_id['Input'].append(target_module)
    if ("db_process" in request.form) and(request.form['db_process'] != ""): 
        target_module = {}
        target_module['module'] = "db_process"
        target_module['_id'] = request.form['db_process']
        raw_id['Input'].append(target_module)
    if ("Module_Input" in request.form) and (request.form['Module_Input'] != ""): 
        input_module = {}
        input_module['module'] = "Module_Input"
        input_module['_id'] = request.form['Module_Input']
        raw_id['Input'].append(input_module)
    if ("OutputReport" in request.form) and (request.form['OutputReport'] != ""): 
        input_module = {}
        input_module['module'] = "OutputReport"
        input_module['_id'] = request.form['OutputReport']
        raw_id['Input'].append(input_module)
    if ("Module_Exploit" in request.form) and (request.form['Module_Exploit'] != ""): 
        input_module = {}
        input_module['module'] = "Module_Exploit"
        input_module['_id'] = request.form['Module_Exploit']
        raw_id['Input'].append(input_module)
    if ("Module_Reconnaissance" in request.form) and (request.form["Module_Reconnaissance"] != "") : 
        recon_module = {}
        recon_module['module']=  "Module_Reconnaissance"
        recon_module['_id'] = request.form['Module_Reconnaissance']
        raw_id['Input'].append(recon_module)
    if "Module[]" in request.form: 
        raw_id['Module']= request.form.getlist('Module[]')
    param = {
        "name": "test_running", 
        "input_raw_id": json.dumps(raw_id)
    }
    
    res = requests.post(const.PUBLIC_API + "/api/v2/module/run", data=param)
    return res.json()

