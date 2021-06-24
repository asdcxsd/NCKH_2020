import re
from requests_toolbelt.utils import dump
import sys,types
from os import urandom,path as ospath,remove as osremove
from lib import database, const
from flask_wtf import CSRFProtect
from flask import Flask, render_template, request, session, jsonify, redirect, url_for, escape,send_from_directory, Markup
from json2html import *
import json
import datetime
import time
import requests
from functools import wraps
app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(0x200)  # cookie encryption
ALLOWED_EXTENSIONS = set(['txt', 'py'])
CSRFProtect(app)
db = database.Database()
listJobs=[]
APIurl = "http://0.0.0.0:5001"
PublicServer = "http://75.119.131.210:5001"



def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not 'logged_in' in session:
            return redirect(url_for('index'))
        elif not session['logged_in']:
            return redirect(url_for('index'))
        else:
            return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

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
    session['account_status'] = db.get_account_status(user_id, username)
    return jsonify({'is_authenticated': True, 'msg': ''})
@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))
@app.route('/pocs')
@login_required
def pocs():
    role = session.get('role')
    if(role == 1): 
        return render_template('pocs.html')
    else: 
        return render_template('403.html')
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
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')






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

@app.route('/uploadReport', methods=['POST'])
@login_required
def uploadReport(): 
    Files = request.files.get('file')
    filename = Files.filename
    targetid = request.form['targetid']
    Files_bytes = Files.read()
    files = {
        "file": (filename, Files_bytes)
        
    }
    data = {
        "target_id":targetid
    }
    headers={'Content-Type': 'multipart/form-data'}
    res = requests.post(APIurl + "/api/v1/reconnaissance/uploadReport",files=files,data=data)
    return res.json()

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
        datenow_format = datetime.datetime.strptime(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'), '%d/%m/%Y %H:%M:%S')
        delta = datenow_format - lastdate_format
        if(delta.days  >=7 ): 
            result = {
                "message": "success", 
                "data":"success to recon", 
                "last_recon": 0
            }
            return result
        else:
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
    data_html = json2html.convert(json = infoFromJson, table_attributes='border="1px solid lightgray" style=" list-style-type: none;margin-left: auto; margin-right: auto; margin-top: 50px; margin-bottom: 50px;table-layout: fixed;"')
    data_html = data_html.replace("target", 'Mục tiêu')
    data_html = data_html.replace("date_start", 'Ngày bắt đầu')
    data_html = data_html.replace("recontool", 'Công cụ sử dụng')
    data_html = data_html.replace('dir</th>', 'Thư mục')
    data_html = data_html.replace("date_end", 'Ngày kết thúc')
    data_html = data_html.replace('port</th>', 'Cổng')
    data_html = data_html.replace("_id", 'ID')
    data_html = data_html.replace("entrypoint", 'Điểm cuối')
    #data_html = data_html.replace("port", 'Cổng')
   
    return data_html 

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
@app.route('/getlastdaycheckcve', methods=['POST'])
@login_required
def getLastDayCheckCve(): 
    targetid = request.form['targetid']
    param = {
        "target_id": targetid
    }
    res = requests.get(APIurl + "/api/v1/pocs/get", params=param)
    result = res.json()
    data = result['data']
    if(len(data) >= 1): 
        lastdate = data[-1]['date_check']; 
        lastdate_format = datetime.datetime.strptime(lastdate, '%d/%m/%Y %H:%M:%S')
        datenow_format = datetime.datetime.strptime(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'), '%d/%m/%Y %H:%M:%S')
        delta = datenow_format - lastdate_format
        if(delta.days  >=7 ): 
            result = {
                "message": "success", 
                "data":"success to check CVE"
            }
            return result
        else:
            result = {
                "message": "fail", 
                "data": str(delta)
            }
            return result
    else: 
        result = {
            "message": "success", 
            "data": "no check CVE available"
        }   
        return result
    


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


##############thuc hien phan upload tool####################
@app.route('/listtool', methods=['GET'])
@login_required
def ListTools(): 
    param = {
        "type": "online"
    }
    res = requests.get(APIurl + "/api/v1/reconnaissance/extension", params=param)
    return res.json()
@app.route("/getavailabletool", methods=['GET'])
@login_required
def GetAvailableTool(): 
    res = requests.get(APIurl + "/api/v1/reconnaissance/loadtool")
    return res.json()
@app.route("/uploadtool", methods=['POST'])
@login_required
def UploadTool(): 
    toolname = request.form['tool']
    data = {
        "filename": toolname
    }
    res = requests.post(APIurl + "/api/v1/reconnaissance/uploadtool", data=data)
    return res.json()
@app.route("/deletetool", methods=['DELETE'])
@login_required
def DeleteTool(): 
    toolname = request.form['tool']
    data = {
        "filename": toolname
    }
    res = requests.delete(APIurl + "/api/v1/reconnaissance/deletetool", data=data)
    return res.json()
###################thuc hien phan pocs######################
@app.route("/fetch-pocs", methods=['GET'])
@login_required
def fetchPOC(): 
    res = requests.get(APIurl + "/api/v1/pocs/info_poc")
    return res.json()
@app.route("/removepoc", methods=['DELETE'])
@login_required
def removePOC(): 
    pocname = request.form['pocname']
    data = {
        "namepoc": pocname
    }
    res = requests.delete(APIurl + "/api/v1/pocs/removepoc", data=data)
    return res.json()
@app.route("/detailpoc", methods=['GET'])
@login_required
def DetailPoc(): 
    pocname = request.args['pocname']
    param = {
        "namepoc": pocname
    }
    res = requests.get(APIurl+ "/api/v1/pocs/detail_poc?", params=param)
    result_json = res.json()
    data = result_json['data']
    data_html = json2html.convert(json = data, table_attributes='border="1px solid lightgray" style="margin-left: auto; margin-right: auto; margin-top: 50px; margin-bottom: 50px;"')
    data_html = data_html.replace("name", 'Tên POC')
    data_html = data_html.replace("version", 'Phiên bản')
    data_html = data_html.replace("author", 'Tác giả')
    data_html = data_html.replace("vulDate", 'Ngày công bố')
    data_html = data_html.replace("createDate", 'Ngày tạo POC')
    data_html = data_html.replace("updateDate", 'Ngày cập nhật')
    data_html = data_html.replace("current_protocol", 'Giao thức')
    data_html = data_html.replace("desc", 'Mô tả')
    data_html = data_html.replace("pocDesc", 'Điểm')
    data_html = data_html.replace("vulType", 'Loại lỗi')
    data_html = data_html.replace("name", 'Tên POC')
    return data_html

@app.route("/uploadpoc", methods=['POST'])
@login_required
def UploadPoc(): 
    Files = request.files.get('file')
    filename = Files.filename
    Files_bytes = Files.read()
    files = {
        "file": (filename, Files_bytes)
        
    }
    headers={'Content-Type': 'multipart/form-data'}
    res = requests.post(APIurl + "/api/v1/pocs/import_poc",files=files)
    return res.json()

if __name__ == '__main__':
    # app.run(host='localhost', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000,debug=True)
   
