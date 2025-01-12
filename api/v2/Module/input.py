from Application.run import delete_data_in_database
import json
from flask import Blueprint, Response, request
from api.v1.output import make_output
from Application.Function.Connect_Database import get_all_input, get_input, remove_data_from_db, remove_input
from bson.json_util import dumps
from bson.objectid import ObjectId
from api.v2.Module.recon import find_date_record

Input = Blueprint('Input', __name__)

@Input.route('/getall', methods=['GET'])
def get_all_input_request(): 
    try: 
        [status, data] = get_all_input()
        if status: 
            result = []
            for cur in data: 
                temp = json.loads(dumps(cur))
                temp['_id'] = temp['_id']['$oid']
                _, temp['date_create'] = find_date_record({"_id": ObjectId(temp['_id_process'])})
                result.append(temp)
            return Response(make_output(data=result, message="success"), mimetype='application/json', status=200)
        else: 
            raise Exception("Can't get module input")
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)

@Input.route("/detail", methods=['POST'])
def get_detail_input_request(): 
    try: 
        query = {}
        if "input_id" in request.form: 
            query['_id'] = ObjectId(request.form['input_id'])
        if "process_id" in request.form: 
            query['_id_process'] = request.form['process_id']
        [status, data] = get_input(query)
        if status and data.count() > 0: 
            result = json.loads(dumps(data))[0]
            _, result['date_create'] = find_date_record({"_id": ObjectId(str(result['_id_process']))})
            result['_id'] = result['_id']['$oid']
            return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
        else: 
            raise Exception("Input not exist")
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)

@Input.route("/remove", methods=['DELETE'])
def delete_input_data_request(): 
    try: 
        if "input_id" in request.form: 
            _id = request.form["input_id"]
            status = delete_data_in_database("Module_Input", _id)
            if status: 
                return Response(make_output(data="Delete input success!", message="success"), mimetype="application/json", status=200)
            else: 
                raise Exception("Delete Input error")
    except Exception as e: 
        return Response(make_output(data=str(e), message="success"), mimetype="application/json", status=404)
