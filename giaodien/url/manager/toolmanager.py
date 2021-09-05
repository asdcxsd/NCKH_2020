from flask import Flask, render_template, request, session, jsonify, redirect, url_for,escape, Blueprint
from functools import wraps
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

ToolManager = Blueprint('ToolManager', __name__)

@ToolManager.route('/quanlicongcu', methods=['GET'])
@login_required
def toolmanager(): 
    return render_template('quanlycongcu.html')

@ToolManager.route('/getalltool',methods=['POST'])
@login_required
def getalltool(): 
    if "module_name" in request.form: 
        module_name = request.form['module_name']
    param = {
        "module_name": module_name
    }
    res = requests.post(const.PUBLIC_API + "/api/v2/managetool/getall", data=param)
    
    return res.json()

@ToolManager.route('/deletetool', methods=['DELETE'])
@login_required
def deletetool(): 
    toolname = request.form['tool']
    data = {
        "filename": toolname
    }
    res = requests.delete(const.PUBLIC_API + "/api/v1/reconnaissance/deletetool", data=data)
    return res.json()