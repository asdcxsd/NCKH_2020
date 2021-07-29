from flask import Blueprint, request, Response
from api.v1.output import make_output

RunShell = Blueprint("RunShell", __name__)

# @RunShell.route("/run", methods=["POST"])
# def run_reverse_shell_poc(): 


@RunShell.route('/runshell', methods=['POST'])
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