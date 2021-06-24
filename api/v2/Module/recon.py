from bson.objectid import ObjectId
from flask import Blueprint, Response, request
from api.v1.output import make_output
from Application.Function.Connect_Database import get_recon, delete_recon
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
        db_process = get_process()
        data_temp['date_start'], data_temp['date_end'] = find_date_record({'_id': ObjectId(str(i['_id_process']))})
            
        result.append(data_temp)
    if status: 
        return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
    else: 
        return Response(make_output(data=str(data), message="fail"), mimetype="application/json", status=404)

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
        status, data  = get_recon(query)
        if data.count == 0 : 
            raise Exception("Not record reconnaissance")
        info_target = data[0]
        _, date = find_date_record({'_id': ObjectId(str(info_target['_id_process']))})
        maxtime = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
        for info in data: 
            date_start, date_end = find_date_record({'_id': ObjectId(str(info['_id_process']))})
            date_check = datetime.strptime(date_end, "%d/%m/%Y %H:%M:%S")
            if date_check > maxtime: 
                maxtime = date_check
                info['date_start'] = date_start
                info['date_end'] = date_end
                info_target = info
        info_target['_id'] = str(info_target['_id'])
        return Response(make_output(data=info_target, message="success"), mimetype="application/json", status=200)
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



        
