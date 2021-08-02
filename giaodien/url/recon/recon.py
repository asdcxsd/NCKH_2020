from types import MethodDescriptorType
from flask import Flask, render_template, request, session, jsonify, redirect, url_for,escape, Blueprint
from functools import wraps
import requests
from .. import const 
import json
import datetime
Recon = Blueprint('Recon', __name__)

def login_required(func): 
    @wraps(func)
    def wrapper(*args, **kwargs): 
        if not "logged_in" in session: 
            return redirect(url_for('Login.login'))
        elif not session['logged_in']: 
            return redirect(url_for('Login.login'))
        else: 
            return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
    
@Recon.route('/recon', methods=['GET'])
@login_required
def thuthapthongtin(): 
    return render_template("recon.html")

@Recon.route('/getallrecon', methods=['GET'])
@login_required
def get_all_recon_request(): 
    res = requests.get(const.PUBLIC_API + "/api/v2/managerecon/getall")
    return res.json()

@Recon.route('/deleterecon', methods=['DELETE'])
@login_required
def delete_recon_request(): 
    if "recon_id" in request.form: 
        param = {
            "recon_id": request.form['recon_id']
        }
        res = requests.delete(const.PUBLIC_API + "/api/v2/managerecon/deleterecon", data=param)
        return res.json()


@Recon.route('/detailrecon', methods=['POST'])
@login_required
def get_detail_recon_request(): 
    if "process_id" in request.form: 
        param = {
            "process_id": request.form['process_id']
        }
        res = requests.post(const.PUBLIC_API + "/api/v2/managerecon/getrecon", data=param)
        return res.json() 


@Recon.route("/getlastrecon", methods=['POST'])
@login_required
def get_last_recon_request(): 
    if "Module_Input" in request.form: 
        param = {
            "input_id": request.form['Module_Input']
        }
        res = requests.post(const.PUBLIC_API + "/api/v2/input/detail", data=param)
        temp = res.json()
        param_request = {
            "target_ip": temp['data']['IN_IP'][0]
        }
        res = requests.post(const.PUBLIC_API + "/api/v2/managerecon/getlastrecon", data=param_request)
        data = res.json()
        if(data['message'] == "success" and (not data['data']) == False): 
            last_time = data['data']['date_end']
            lastdate_format = datetime.datetime.strptime(last_time, '%d/%m/%YT%H:%M:%S')
            datenow_format = datetime.datetime.strptime(datetime.datetime.now().strftime('%d/%m/%YT%H:%M:%S'), '%d/%m/%YT%H:%M:%S')
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
                    "message": "success", 
                    "data":"success to recon", 
                    "last_recon": 0
                }
            return result

