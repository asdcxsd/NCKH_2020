
from datetime import datetime
import json
from flask import Blueprint, Response, request
from Database.database import get_recon, delete_recon, reconnaissance
from api.v1.output import make_output
from bson.objectid import ObjectId
from threading import Thread
from Library.Reconnai.reconnaissance import Reconnaissance
from Library.Target.target import get_target_url
Recon = Blueprint('recon', __name__)
import xml.etree.ElementTree as ET

@Recon.route('/get', methods=['GET'])
def request_get_reconnaissance():
    query = {}
    if "target_id" in request.args:
        target_id = request.args['target_id']
        query["target_id"]  = target_id
    if "_id" in request.args:
        _id = request.args['_id']
        query["_id"]  = ObjectId(_id)

    [status, data] = get_recon(query)
    result = []
    for i in range(data.count()):
        temp = data[i];
        temp['_id'] = str(temp['_id'])
        result.append(temp)
    if status :
        return Response(make_output(data = result, message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= str(result) ), mimetype="application/json", status=404)

@Recon.route('/getall', methods=['GET'])
def request_get_all_reconnaissance():
 
    [status, data] = get_recon({})
    result = []
    for i in data:
        temp = {}
        temp['_id'] = str(i['_id'])
        temp['target_id'] = i['target_id']
        temp['date_start'] = i['date_start']
        temp['date_end'] = i['date_end']
        result.append(temp)
    if status :
        return Response(make_output(data = result, message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= str(result) ), mimetype="application/json", status=404)


@Recon.route('/delete', methods=['DELETE'])
def request_delete_reconnaissance():
    reconnaissance_id = request.args['reconnaissance_id']
    status = delete_recon({"_id": ObjectId(reconnaissance_id)})
   
    if status :
        return Response(make_output(data = "delete reconnaissance susscess", message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= str(status) ), mimetype="application/json", status=404)


global reconnaissance_running 
reconnaissance_running = []
def run_reconnaissance_thread(target_id, extension, reports):
    global reconnaissance_running
    Recon  = Reconnaissance()
    Recon.update_target(target_id)
    Recon.update_extension(extension)
    Recon.update_report(reports)
    runthread = Thread(target=Recon.thread_run, args=())
    runthread.start()
    reconnaissance_running.append({"thread": runthread, "target_id": target_id, "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S") , "status": "running"})

@Recon.route('/start', methods=['PUT'])
def request_put_reconnaissance():
    try:
        target_id = request.form['target_id']
        if 'extension' in request.form:
            extension = request.form['extension']
        else: 
            extension = ''
        if "report" in request.form:
            try:
                reports = json.loads(request.form['report'])['report']
            except Exception as e:
                raise Exception("Report error fomat" + str(e))
        else: 
            reports = []
        run_reconnaissance_thread(target_id, extension, reports)

        return Response(make_output(data = "start reconnaissance susscess", message ='success'), mimetype="application/json", status=200)
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)

@Recon.route('/status', methods=['GET'])
def request_status_reconnaissance():
    global reconnaissance_running
    result = []
    for run in reconnaissance_running:
        if run['thread'].isAlive():
            result.append({'target_id': run['target_id'], 'date' : run['date'], 'status': "running"})
        else:
            result.append({'target_id': run['target_id'], 'date' : run['date'], 'status': "success"})
           
    if len(result) :
        return Response(make_output(data = result, message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= "No data" ), mimetype="application/json", status=404)


@Recon.route('/extension', methods=['GET'])
def request_get_extension_reconnaissance():
    try:
        if "type" in request.args:
            request_type = request.args['type']
        else: request_type = "offline"
        result = Reconnaissance.get_all_extension()
        ans = []
        for fo in result:
            func = fo.reconnaissance()
            info = func.info()
            if info['type'] == request_type or request_type == "offline":
                ans.append(info)

        return Response(make_output(data = ans, message ='success'), mimetype="application/json", status=200)
    except Exception as e:
        return Response(make_output(message =  "fail", data= "No data" ), mimetype="application/json", status=404)