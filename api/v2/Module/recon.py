from bson.objectid import ObjectId
from flask import Blueprint, Response, request
from api.v1.output import make_output
from Application.Function.Connect_Database import get_recon,get_module_input ,  delete_recon,get_ip_record
from bson.json_util import dumps
import json
from Application.Function.DB_Process import get_process
from datetime import datetime

ManageRecon = Blueprint('ManageRecon', __name__)


def find_date_record(data): 
    db_process = get_process(data)
    data_process  = json.loads(dumps(db_process))[1][0]
    if data_process['Status'] == "StatusSuccess": 
        return data_process['Date_Create'], data_process['Date_Stop']

@ManageRecon.route('/getall', methods=["GET"])
def request_get_all_reconnaissance(): 
    [status, data] = get_recon({})
    result = []
    for i in data: 
        data_temp = json.loads(dumps(i))
        data_temp['date_start'], data_temp['date_end'] = find_date_record({'_id': ObjectId(str(i['_id_process']))})
        module_input = data_temp["pre_type_module"][0]["_id"]
        status, data_temp_ip = get_ip_record(module_input)
        if status: 
            data_temp["ip"] = data_temp_ip
        result.append(data_temp)
    if status: 
        return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
    else: 
        return Response(make_output(data=str(data), message="fail"), mimetype="application/json", status=404)

@ManageRecon.route("/getrecon", methods=['POST'])
def request_get_recon_result(): 
    try: 
        if "process_id" in request.form: 
            process_id = request.form['process_id']
            query = {}
            query['_id_process'] = process_id
            _,result = get_recon(query)
            result = json.loads(dumps(result))[0]
            result['_id'] = str(result["_id"]) 
            result['date_start'], result['date_stop'] = find_date_record({"_id": ObjectId(process_id)})
            module_input = result["pre_type_module"][0]["_id"]
            status, data_temp_ip = get_ip_record(module_input)
            if status: 
                result["ip"] = data_temp_ip
            return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)

@ManageRecon.route('/getlastrecon', methods=['POST'])
def request_get_last_recon(): 
    try:
        query = {}
        if "target_ip" in request.form: 
            query['IN_IP'] = request.form['target_ip']
        if "target_domain" in request.form: 
            query['IN_DOMAIN'] = request.form['target_domain']
        if "target_name" in request.form: 
            query['IN_NAME'] = request.form['target_name']
        status, data  = get_module_input(query)
        if status: 
            lasttime = datetime.strptime("01/01/1970T00:00:00","%d/%m/%YT%H:%M:%S")
            lasttime_module_input_id = ""
            for i in data:  
                module_input = json.loads(dumps(i))
                module_input_id = module_input["_id"]["$oid"]
                query_recon = {
                    "pre_type_module": [
                        {
                            "module": "Module_Input",
                            "_id": module_input_id
                        }
                    ]
                }
                status, data = get_recon(query_recon)
                if status: 
                    data = data[0]
                    data['date_start'], data['date_end'] = find_date_record({'_id': ObjectId(str(data['_id_process']))})
                    date_check = datetime.strptime(data['date_end'], "%d/%m/%YT%H:%M:%S")
                    if date_check > lasttime: 
                        lasttime = date_check
                        lasttime_module_input_id = module_input_id
            query_recon = {
                    "pre_type_module": [
                        {
                            "module": "Module_Input",
                            "_id": lasttime_module_input_id
                        }
                    ]
                }
            status, data = get_recon(query_recon)
            if status: 
                result = json.loads(dumps(data))[0]
                result["_id"] = str(result['_id'])
                result["date_start"], result['date_end'] = find_date_record({'_id': ObjectId(str(result['_id_process']))})
                module_input = result["pre_type_module"][0]["_id"]
                status, data_temp_ip = get_ip_record(module_input)
                if status: 
                    result["ip"] = data_temp_ip
                return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)

@ManageRecon.route('/deleterecon', methods=["DELETE"])
def request_delete_recon(): 
    try: 
        if "recon_id" in request.form: 
            recon_id = request.form['recon_id']
            status = delete_recon({"_id": ObjectId(recon_id)})
        if status: 
            return Response(make_output(data="delete recon success", message="success"), mimetype="application/json", status=200)
        else: 
            raise Exception(status)
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)



        
