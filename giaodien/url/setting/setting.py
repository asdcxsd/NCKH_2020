from flask import Flask, render_template, request, session, jsonify, redirect, url_for,escape, Blueprint
from functools import wraps
from url.login.login import Login
import requests
from .. import const

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

Setting = Blueprint('Setting', __name__)


@Setting.route('/setting', methods=['GET'])
@login_required
def setting(): 
    return render_template('setting.html')

@Setting.route('/addsetting', methods=['POST'])
@login_required
def addsetting(): 
    param = {}
    if ("Cf_PublicIP" in request.form) and(len(request.form['Cf_PublicIP']) != 0 ): 
        param['Cf_PublicIP'] = request.form['Cf_PublicIP']
    if ("Cf_Username_VPS" in request.form) and (len(request.form['Cf_Username_VPS']) != 0 ): 
        param['Cf_Username_VPS'] = request.form['Cf_Username_VPS']
    if ("Cf_Password_VPS" in request.form) and (len(request.form['Cf_Password_VPS']) != 0): 
        param['Cf_Password_VPS'] = request.form['Cf_Password_VPS']
    if ("Cf_PublicPort" in request.form) and (len(request.form['Cf_PublicPort']) != 0 ): 
        param['Cf_PublicPort'] = request.form['Cf_PublicPort']
    if ("Cf_Host_Check_Connect" in request.form) and(len(request.form['Cf_Host_Check_Connect']) != 0): 
        param['Cf_Host_Check_Connect'] = request.form['Cf_Host_Check_Connect']
    if( "Cf_Server_OpenPort" in request.form) and(len(request.form['Cf_Server_OpenPort']) != 0): 
        param['Cf_Server_OpenPort'] = request.form['Cf_Server_OpenPort']
    if ("Cf_Host_Check_Metasploit_AI" in request.form) and (len(request.form['Cf_Host_Check_Metasploit_AI']) != 0 ): 
        param['Cf_Host_Check_Metasploit_AI'] = request.form['Cf_Host_Check_Metasploit_AI']
    if ("Cf_Server_Metasploit_OpenPort" in request.form) and(len(request.form['Cf_Server_Metasploit_OpenPort']) != 0): 
        param['Cf_Server_Metasploit_OpenPort'] = request.form['Cf_Server_Metasploit_OpenPort']    
    param['Cf_Account_id'] = session['user_id']
    print(param)
    res = requests.post(const.PUBLIC_API + "/api/v2/module/config", data=param)
    result = res.json()
    if (result['message'] == 'success'): 
        session['config_id'] = result['data']
    return res.json() 

    