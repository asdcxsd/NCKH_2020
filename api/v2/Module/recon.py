from bson.objectid import ObjectId
from flask import Blueprint, Response, request
from api.v1.output import make_output
from Application.Function.Connect_Database import get_recon ,  delete_recon,get_ip_record
from bson.json_util import dumps
import json
from Application.Function.DB_Process import get_process
from Application.run import dump_all_data_from_db, delete_data_in_database
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
        try:
            data_temp = json.loads(dumps(i))
            data_temp['date_start'], data_temp['date_end'] = find_date_record({'_id': ObjectId(str(i['_id_process']))})
            module_recon_id = str(i["_id"])
            data_from_db = dump_all_data_from_db("Module_Reconnaissance", module_recon_id)
            data_temp["target_ip"] = data_from_db["IN_IP"]
            data_temp["target_domain"] = data_from_db['IN_DOMAIN']
            data_temp["_id"] = data_temp['_id']['$oid']
            result.append(data_temp)
        except:
            pass
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
            result['date_start'], result['date_stop'] = find_date_record({"_id": ObjectId(process_id)})
            data_from_db = dump_all_data_from_db("Module_Reconnaissance", str(result["_id"]["$oid"]))
            result["target_ip"] = data_from_db["IN_IP"]
            result["target_domain"] = data_from_db['IN_DOMAIN']
            result['_id'] = result["_id"]['$oid']
            return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)

@ManageRecon.route('/getlastrecon', methods=['POST'])
def request_get_last_recon(): 
    try:
        lasttime = datetime.strptime("01/01/1970T00:00:00","%d/%m/%YT%H:%M:%S")
        query = {}
        if "target_ip" in request.form: 
            query['IN_IP'] = request.form['target_ip']
        status, data  = get_recon({})
        result = {}
        for i in data: 
            data_temp = json.loads(dumps(i))
            data_temp['date_start'], data_temp['date_end'] = find_date_record({'_id': ObjectId(str(i['_id_process']))})
            time_check = datetime.strptime(data_temp['date_end'],"%d/%m/%YT%H:%M:%S")
            if time_check > lasttime: 
                lasttime = time_check
                module_recon_id = str(i["_id"])
                data_from_db = dump_all_data_from_db("Module_Reconnaissance", module_recon_id)
                if query["IN_IP"] == data_from_db["IN_IP"][0]: 
                    data_temp["target_ip"] = data_from_db["IN_IP"]
                    data_temp["target_domain"] = data_from_db["IN_DOMAIN"]
                    result = data_temp
                    result["_id"] = str(result["_id"]['$oid'])
        return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)





@ManageRecon.route('/deleterecon', methods=["DELETE"])
def request_delete_recon(): 
    try: 
        if "process_id" in request.form: 
            process_id = request.form['process_id']
            query = {}
            query['_id_process'] = process_id
            status, data = get_recon(query)
            if status: 
                data = data[0]
                result = json.loads(dumps(data))
                module_recon_id = result["_id"]['$oid']
                print(result)
                print(module_recon_id)
            status = delete_data_in_database("Module_Reconnaissance", module_recon_id)
            if not status:
                raise Exception("do not have that record")
            return Response(make_output(data="delete record success", message="success"), mimetype="application/json", status=200)
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)



        
