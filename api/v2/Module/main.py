
from Application.Account import config_update_by_id, delete_config_with_id, get_account, get_config_query, get_account_for_update, update_user_password
import json
from Application.Function.Connect_Database import get_all_process, get_recon, get_exploit_cve, get_input, get_shell_log_data, get_process_with_query
from bson.json_util import dumps
import threading
from Application.Function.Connect_Framework import get_class_module
from Application.Process_running import ProcessRunning
from urllib.parse import urlparse
from bson.objectid import ObjectId
from flask import Blueprint, Response, request
from api.v1.output import make_output
from Framework.Framework import Framework
from Application.Input.target import get_target
from Application.run import RunFrammework, delete_data_in_database
Main = Blueprint('Main', __name__)

# run all function
Array_Save_Running_Session = []

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
                each_data['Module'] = temp['Module']
                result.append(each_data)
            return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
        else: 
            raise Exception('Can not get data')
    except Exception as e: 
        return Response(make_output(message="fail", data=str(e)), mimetype="application/json", status=404)

@Main.route("/timeruntoolofinput", methods=['POST'])
def get_datetime_of_tool_run_with_input(): 
    try: 
        if "input_ip" in request.form: 
            query = {}
            query["Target"] = request.form['input_ip']
            status, data = get_process_with_query(query)
            if status: 
                result = []
                list_tool_name = []
                data = json.loads(dumps(data))
                for i in range(len(data)-1, -1, -1) :
                    temp = data[i] 
                    list_module = temp["Module"]
                    for module in list_module: 
                        each_data = {}
                        each_data["Date_Stop"] = temp['Date_Stop']
                        each_data['module_name'] = module
                        if module not in list_tool_name: 
                            result.append(each_data)
                            list_tool_name.append(module)    
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
        print(request.form)
        if "input_raw_id" in request.form: 
            input_raw_id = request.form['input_raw_id']
            if "name" in request.form:
               name_run = request.form['name']
            else:
                name_run = "No Name"
            input_json_id = json.loads(input_raw_id)
            proRunning = ProcessRunning(name_run)
            FrameworkRun = RunFrammework()
            data = {"_id": proRunning._id,
                "frameRun":FrameworkRun }
            Array_Save_Running_Session.append(data)
            #Array_Save_Running_Session[-1]["frameRun"].Init()
            def thread_run(proRunning, input_json_id):
                Array_Save_Running_Session[-1]["frameRun"].Run(proRunning, input_json_id )
                #print(id(Array_Save_Running_Session[-1]))
            threading.Thread(target=thread_run, args=(proRunning, input_json_id, )).start()
            dataResult['_id'] = proRunning._id
        else: raise Exception("Target not exist!")
        return Response(make_output(data = dataResult, message ='success'), mimetype="application/json", status=200)
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)

@Main.route('/stop', methods=['POST'])
def stop_framework():
    try:
        _id = request.form['_id']
        dataResult = {
                "status": "error"
            }
        for proRun in Array_Save_Running_Session:
            if _id == proRun["_id"]:
                proRun["frameRun"].Stop();
                dataResult = {
                    "status": "success"
                }
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
        data = get_account(username, password)
        _id = str(data['_id'])
        role = data['role']
        if _id == False:
            message = 'Login Fail'
            data = {
                "message" : "username or password wrong!!"
            }
        else:
            message = 'Login Success'
            data = {
                "_id" : _id, 
                "role": role
            }

        return Response(make_output(data = data, message =message), mimetype="application/json", status=200)
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)

@Main.route('/dashboardinfo', methods=['GET'])
def get_dashboard_info_request(): 
    try: 
        [status, target] = get_target({})
        if status: 
            target_count = target.count()
        [status, account] = get_account_for_update({})
        if status: 
            account_count = account.count()
        [status, data] = get_exploit_cve({})
        if status: 
            vul_count = 0
            for cur in data: 
                temp = json.loads(dumps(cur))
                if "EXPLOIT_POCS" in temp: 
                    vul_count += len(temp["EXPLOIT_POCS"])
                if "EXPLOIT_METASPLOIT_AI" in temp: 
                    vul_count += len(temp["EXPLOIT_METASPLOIT_AI"])
        [status, data] = get_all_process()
        if status: 
            process_running_count = 0 
            for cur in data: 
                temp = json.loads(dumps(cur))
                if temp['Status'] == "StatusRunning": 
                    process_running_count += 1
        data_for_return = {
            "target": target_count, 
            "account": account_count, 
            "vulnerability": vul_count, 
            "process": process_running_count 
        }
        return Response(make_output(message="success", data=data_for_return), mimetype="application/json", status=200)
    except Exception as e: 
        return Response(make_output(message="fail", data=str(e)), mimetype="application/json", status=404)


@Main.route("/processdashboard", methods=['GET'])
def get_process_dashboard(): 
    try: 
        status, data = get_all_process()
        if status: 
            process_count = {}
            for cur in data: 
                temp = json.loads(dumps(cur))
                month_process = temp['Date_Create'].split("T")[0][3:]
                if month_process not in process_count: 
                    process_count[month_process] = 1
                else: 
                    process_count[month_process] += 1
            return Response(make_output(data = process_count, message="success"), mimetype="application/json", status=200)
    except Exception as e: 
        return Response(make_output(message="fail", data=str(e)), mimetype="application/json", status=404)


@Main.route("/pocdashboard", methods=['GET'])
def get_poc_dashboard(): 
    try: 
        ClassPOCCheck = get_class_module("PocCheck", "module")
        objectPOCCheck = ClassPOCCheck()
        listPOC = objectPOCCheck.get_all_pocs()
        list_detail_POC = []
        for i in listPOC: 
            temp = objectPOCCheck.get_info_pocs(i)
            poc_detail = {}
            poc_detail['appVersion'] = temp["appVersion"]
            poc_detail['appName'] = temp['appName']
            poc_detail['createDate'] = temp['createDate']
            poc_detail['desc'] = temp['desc']
            list_detail_POC.append(poc_detail)
        return Response(make_output(data=list_detail_POC, message="success"), mimetype="application/json", status=200)
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)




@Main.route("/changepassword", methods=['POST'])
def change_password_request(): 
    try: 
        if "currentpassword" in request.form: 
            currentpassword = request.form['currentpassword']
        if "newpassword" in request.form: 
            newpassword = request.form['newpassword'] 
        if "Account_id" in request.form: 
            user_id = request.form['Account_id']
        query = {}
        query['_id'] = ObjectId(user_id)
        status, data = get_account_for_update(query)
        if status: 
            result = json.loads(dumps(data[0]))
            user_current_password = result['password']
            if user_current_password != currentpassword: 
                raise Exception("currentpassword is incorrect")
            else: 
                query = {}
                query['_id'] = ObjectId(user_id)
                query['password'] = newpassword
                status, data = update_user_password(query)
                if status: 
                    return Response(make_output(message =  "success", data="success"), mimetype="application/json", status=404)
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


@Main.route("/delete", methods=["DELETE"])
def delete_module_record(): 
    try: 
        if "process_id" in request.form: 
            process_id = request.form['process_id']
            print("process_id" + process_id)
        status = delete_data_in_database("db_process", process_id)
        if not status:
            raise Exception("do not have that record")
        return Response(make_output(data="delete record success", message="success"), mimetype="application/json", status=200)
    except Exception as e : 
        print(e)
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)
