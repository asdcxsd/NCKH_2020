
import datetime
import string
from flask import Blueprint, Response, request
from pymongo import results
from database import get_recon
from api.v1.output import make_output
from POCURI import POCURI
Poc = Blueprint('Poc', __name__)
import xml.etree.ElementTree as ET
from threading import Thread
from target import get_target_url
from runpoc import run_scan

@Poc.route('/tools', methods=['GET'])
def get_all_tools():
    CPOC = POCURI()
    result = CPOC.get_all_pocs()
    print(result)
    if not isinstance(result, str):
        return Response(make_output(data = result, message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= result ), mimetype="application/json", status=404)


@Poc.route('/get', methods=['GET'])
def get_all_tools():
    CPOC = POCURI()
    result = CPOC.get_all_pocs()
    print(result)
    if not isinstance(result, str):
        return Response(make_output(data = result, message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= result ), mimetype="application/json", status=404)

def checkpoc_run(target_id, pocs):
    check_pocs = run_scan(target_id=target_id)
    check_pocs.run()

global checkpoc_running 
checkpoc_running = []

@Poc.route('/start', methods=['PUT'])
def request_put_runpoc():
    target_id = request.form['target_id']
    if 'pocrun' in request.form:
        run_pocs = request.form['pocrun']
    else: 
        run_pocs = '*telerik_cve_2019_18935*'
    global checkpoc_running
    [status, url_target] = get_target_url(target_id)
    if status :
        runthread = Thread(target=checkpoc_run, args=(target_id, run_pocs, ))
        runthread.start()
        checkpoc_running.append({"thread": runthread, "target_id": target_id, "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S") })
        return Response(make_output(data = "start reconnaissance susscess", message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= str(status) ), mimetype="application/json", status=404)

@Poc.route('/status', methods=['GET'])
def request_status_runpoc():
    global checkpoc_running
    result = []
    temp_recon = []
    for run in checkpoc_running:
        if run['thread'].isAlive():
            result.append({'target_id': run['target_id'], 'date' : run['date']})
            temp_recon.append(run)
    checkpoc_running = temp_recon
    if len(result) :
        return Response(make_output(data = result, message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= "No data" ), mimetype="application/json", status=404)

