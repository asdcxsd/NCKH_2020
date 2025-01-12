
from datetime import datetime
import json
import string, random # for gen random id
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
    try:
        if "reconnaissance_id" in request.args:
            reconnaissance_id = request.args['reconnaissance_id']
            status = delete_recon({"_id": ObjectId(reconnaissance_id)})
        if "target_id" in request.args:
            target_id = request.args['target_id']
            status = delete_recon({"target_id": target_id})
        if status ==True :
            return Response(make_output(data = "delete reconnaissance susscess", message ='success'), mimetype="application/json", status=200)
        else: raise Exception(status)
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)


global reconnaissance_running
reconnaissance_running = []
def update_status_reconnaissance_running(_id, status,summary = {}, target_id =None, runthread=None,  recon_id="No"):
    global reconnaissance_running
    if _id in [_['_id'] for _ in reconnaissance_running]:
        #update 
        vt = [_['_id'] for _ in reconnaissance_running].index(_id)
        reconnaissance_running[vt]['recon_id']  = recon_id 
        reconnaissance_running[vt]['status'] = status
    else: 
        date =  datetime.now().strftime("%d/%m/%Y %H:%M:%S") 
        reconnaissance_running.append({"_id": _id, "thread": runthread, "summary" : summary,  "target_id": target_id, 'recon_id':recon_id , 'date': date, "status": status})
        

def func_thread_recon(Recon, _id_session):
    recon_id = Recon.thread_run()
    recon_id = str(Recon._id)
    
    update_status_reconnaissance_running(_id=_id_session, status="success", recon_id=recon_id)
def run_reconnaissance_thread(target_id, extension, reports):
    global reconnaissance_running
    Recon  = Reconnaissance()
    Recon.update_target(target_id)
    Recon.update_extension(extension)
    Recon.update_report(reports)
    _id_session = ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
    runthread = Thread(target=func_thread_recon, args=(Recon, _id_session))
    runthread.start()

    summary = {
        "Toolsrecon": Recon.recon_extensions,
        "Report" : Recon.recon_reports
    }
    update_status_reconnaissance_running(_id=_id_session, summary=summary,  status="running", target_id=target_id, runthread=runthread)
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
        result.append({"_id": run['_id'], 'target_id': run['target_id'], "summary" : run['summary'],  'date' : run['date'], 'recon_id' : run['recon_id'], 'status':  run['status']})
           
    if len(result) :
        return Response(make_output(data = result, message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= "No data" ), mimetype="application/json", status=404)


@Recon.route('/lastrecon', methods=['GET'])
def request_get_lastrecon_reconnaissance():
    try:
        if "target_id" in request.args:
            target_id = request.args['target_id']
        else: raise Exception("Don't exist target!")

        data_find = {
            "target_id": target_id
        }
        # get reconnai last if return multi reconnai
        status, data = get_recon(data_find)
        if data.count() == 0:
            raise Exception ("Not recond reconnaissance")
        info_target = data[0]
        date = info_target['date_end']
        maxtime = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
        for info in data:
            date = info['date_end']
            date = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
            if (date > maxtime):
                maxtime = date
                info_target = info 
                
        info_target["_id"] = str(info_target["_id"] )

        return Response(make_output(data = info_target, message ='success'), mimetype="application/json", status=200)
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)

               