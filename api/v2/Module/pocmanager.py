from flask import Blueprint, Response, request
from api.v1.output import make_output
import json
from bson.json_util import dumps
from Application.Function.Connect_Database import get_exploit_cve

ManagePOC = Blueprint("ManagePOC", __name__)

@ManagePOC.route('/getall', methods=['GET'])
def get_all_poc_check(): 
    [status, data] = get_exploit_cve({})
    if data.count() == 0 : 
        raise Exception(status)
    result = []
    for i in data: 
        i['_id'] = str(i['_id'])
        result.append(i)
    if status:
        return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
    else: 
        return Response(make_output(data=result, message="fail"), mimetype="application/json", status=404)

