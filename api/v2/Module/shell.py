from flask import Blueprint, request, Response
from api.v1.output import make_output
import json
from Application.Process_running import ProcessRunning
from Application.run import RunFrammework
import threading
from Application.Function.Connect_Database import get_shell_log_data
from bson.json_util import dumps

RunShell = Blueprint("RunShell", __name__)

# @RunShell.route("/run", methods=["POST"])
# def run_reverse_shell_poc(): 


# @RunShell.route('/runshell', methods=['POST'])
# def running():
#     dataResult = {}
#     try:
#         if "input_raw_id" in request.form: 
#             input_raw_id = request.form['input_raw_id']
#             if "name" in request.form:
#                name_run = request.form['name']
#             else:
#                 name_run = "No Name"
#             input_json_id = json.loads(input_raw_id)
#             proRunning = ProcessRunning(name_run)
#             FrameworkRun = RunFrammework()
#             def thread_run(proRunning, input_json_id):
#                 FrameworkRun.Run(proRunning, input_json_id )
#             threading.Thread(target=thread_run, args=(proRunning, input_json_id, )).start()
#             dataResult['_id'] = proRunning._id
#         else: raise Exception("Target not exist!")
#         return Response(make_output(data = dataResult, message ='success'), mimetype="application/json", status=200)
#     except Exception as e:
#         return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)

@RunShell.route("/getshelllogstatus", methods=['POST'])
def get_shell_log_after_running_request(): 
    try: 
        query = {}
        if "process_id" in request.form: 
            query['_id_process'] = request.form['process_id']
            status, data = get_shell_log_data(query)
            if status and data.count() > 0: 
                result = json.loads(dumps(data))[0]
                print(result)
                status1 = result['OUTPUT_LOG_RUN_SHELL'][0]['status']
                
                return Response(make_output(data = status1, message="success"),mimetype="application/json", status=200)
            else: 
                raise Exception("Error on connect to database!")
    except Exception as e: 
        return Response(make_output(message="fail", data=str(e)), mimetype="application/json", status=404)

@RunShell.route("/getinforsevershell", methods=['POST'])
def get_server_shell_infor_data(): 
    try: 
        query = {}
        if "process_id" in request.form: 
            query['_id_process'] = request.form['process_id']
            status, data = get_shell_log_data(query)
            if status and data.count() > 0: 
                result = json.loads(dumps(data))[0]['OUTPUT_LOG_RUN_SHELL'][0]
                return Response(make_output(data=result, message="success"),mimetype="application/json", status=200)
            else: 
                raise Exception("Error to connect to database!")
    except Exception as e : 
        return Response(make_output(message="fail", data=str(e)), mimetype="application/json", status=404)

@RunShell.route("/getshelllogdata", methods=['POST'])
def get_shell_log_data_request(): 
    try: 
        query = {}
        if "id_process" in request.form: 
            query['_id_process'] = request.form['id_process']; 
            status, data= get_shell_log_data(query)
            if status: 
                result = json.loads(dumps(data))[0]
                result['_id'] = result['_id']['$oid']
                return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
            else: 
                raise Exception("Error on connect to database!")
    except Exception as e:
        return Response(make_output(message="fail", data=str(e)), mimetype="application/json", status=404) 
