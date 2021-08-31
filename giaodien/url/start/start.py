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


@Start.route('/run', methods=['POST'])
@login_required
def run_module(): 
    raw_id = {}
    raw_id['Input'] = []
    config_module = {}
    config_module['module'] = "ConfigSetup"
    config_module["_id"] = session['config_id']
    raw_id['Input'].append(config_module)
    if "Target" in request.form: 
        target_module = {}
        target_module['module'] = "Target"
        target_module['_id'] = request.form['Target']
        raw_id['Input'].append(target_module)
    if "Module_Input" in request.form: 
        input_module = {}
        input_module['module'] = "Module_Input"
        input_module['_id'] = request.form['Module_Input']
        raw_id['Input'].append(input_module)
    if "Module_Reconnaissance" in request.form: 
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
    print(json.dumps(raw_id))
    res = requests.post(const.PUBLIC_API + "/api/v2/module/run", data=param)
    return res.json()

