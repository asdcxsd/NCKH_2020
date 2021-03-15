
from datetime import datetime
from flask import Blueprint, Response, request
from Database.database import get_recon, delete_recon, reconnaissance
from api.v1.output import make_output
from bson.objectid import ObjectId
from threading import Thread
from Library.Reconnai.reconnaissance import thread_run as reconnaissance_run
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

@Recon.route('/start', methods=['PUT'])
def request_put_reconnaissance():
    target_id = request.form['target_id']
    if 'extension' in request.form:
        extension = request.form['extension']
    else: 
        extension = '*wappalyzer*'
    global reconnaissance_running
    [status, url_target] = get_target_url(target_id)
    if status :
        runthread = Thread(target=reconnaissance_run, args=(url_target, extension, ))
        runthread.start()
        reconnaissance_running.append({"thread": runthread, "target_id": target_id, "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S") })
        return Response(make_output(data = "start reconnaissance susscess", message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= str(status) ), mimetype="application/json", status=404)

@Recon.route('/status', methods=['GET'])
def request_status_reconnaissance():
    global reconnaissance_running
    result = []
    temp_recon = []
    for run in reconnaissance_running:
        if run['thread'].isAlive():
            result.append({'target_id': run['target_id'], 'date' : run['date']})
            temp_recon.append(run)
    reconnaissance_running = temp_recon
    if len(result) :
        return Response(make_output(data = result, message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= "No data" ), mimetype="application/json", status=404)


from Library.Reconnai.reconnaissance import get_all_extension
@Recon.route('/extension', methods=['GET'])
def request_get_extension_reconnaissance():
    result = get_all_extension()
    ans = []
    for fo in result:
        func = fo.reconnaissance()
        ans.append(func.info())

    if len(result) :
        return Response(make_output(data = ans, message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= "No data" ), mimetype="application/json", status=404)

