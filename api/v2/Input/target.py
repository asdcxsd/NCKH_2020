

from urllib.parse import urlparse
from bson.objectid import ObjectId
from flask import Blueprint, Response, request
from Application.Function.Connect_Database import delete_recon
from Application.Input.target import get_target_url, get_target, put_target, delete_target,  InputTarget, update_target
from api.v1.output import make_output
Target = Blueprint('Target', __name__)
import xml.etree.ElementTree as ET
import json
from bson import json_util

@Target.route('/gettarget', methods=['GET'])
def get_url_by_id():
    try:
        target_id = request.args['target_id']
        [status, data]  = get_target_url(target_id)
        temp = json_util.dumps(data)
        data = json.loads(temp)
        data['_id'] = data['_id']["$oid"]
        if status :
            return Response(make_output(data = data, message ='success'), mimetype="application/json", status=200)
        else:
            raise Exception("Target not exist!")
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)

@Target.route('/getall', methods=['GET'])
def request_get_all_target():
    try:
        [status, cursor] = get_target({})
        list_cur = list(cursor)
        result = []
        for cur in list_cur:
            temp = json_util.dumps(cur)
            jsonnew = json.loads(temp)
            jsonnew['_id'] = jsonnew['_id']["$oid"]
            result.append(jsonnew)
        if status :
            return Response(make_output(data = result, message ='success'), mimetype="application/json", status=200)
        else:
            raise Exception(result)
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)

@Target.route('/insert', methods=['POST'])
def request_put_target():
    try:
        input_request = InputTarget()
        if "ip_address" in request.form:
            input_request.ip_address = request.form['ip_address']
        if "domain" in request.form:
            input_request.domain = request.form['domain']
        if "describe" in request.form:
            input_request.describe = request.form['describe']
        if "authen" in request.form:
            try:
                input_request.authen = json.loads(request.form['authen'])
            except Exception as e:
                print("Error input authen: ", e)
        input_request.name = request.form['name']
        json_input = input_request.to_json()
        [status, data] = get_target({'name': input_request.name})
        if data.count()== 0:
            result = put_target(json_input)
        else:
            raise Exception("Name exist!")
        if status ==True :
            return Response(make_output(data = "Update success", message = str(result.inserted_id)), mimetype="application/json", status=200)
        else: 
            raise Exception("Insert Error")
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)


@Target.route('/update', methods=["POST"])
def update_target_request(): 
    try: 
        if "target_id" in request.form: 
            [status, data]= get_target({"_id": ObjectId(request.form['target_id'])})
            if status == False: 
                raise Exception("Find target error!")
            else: 
                target_request = InputTarget()
                if "name" in request.form: 
                    target_request.name = request.form['name']
                if "ip_address" in request.form: 
                    target_request.ip_address = request.form['ip_address']
                if "domain" in request.form: 
                    target_request.domain = request.form['domain']
                if "describe" in request.form: 
                    target_request.describe = request.form['describe']
                if "authen" in request.form: 
                    target_request.authen = json.loads(request.form['authen'])
                result  = update_target( {"_id": ObjectId(request.form['target_id'])},target_request.to_json())
                if result.modified_count > 0: 
                    return Response(make_output(data = 'Update target success', message="success"), mimetype="application/json", status=200)
                else: 
                    raise Exception('Update target error!!')
    except Exception as e: 
        return Response(make_output(data="Update target fail!", message="fail"), mimetype="application/json", status=404)
        
    except Exception as e: 
        return Response(make_output(message="fail", data=str(e)), mimetype='application/json', status=404)

@Target.route('/delete', methods=['DELETE'])
def request_delete_target():
    try:
        data_remove = {}
        if "target_id" in request.form: 
            target_id = request.form['target_id']
            data_remove['_id'] = ObjectId(target_id)
        [status, data] = get_target(data_remove)
        if status == False: raise Exception(data)
        if (data.count() > 0):
            status= delete_target(data_remove)
            if "_id" in data_remove:
                data_remove = {'target_id': str(data_remove['_id'])}
                status = delete_recon(data_remove)
            #delete all 

            #dedlete all --
        else: raise Exception("Target not exist!")
        return Response(make_output(data = "delete success", message ='success'), mimetype="application/json", status=200)
    except Exception as e:    
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)


