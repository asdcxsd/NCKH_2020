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

@ToolManager.route('/getalltool',methods=['GET'])
@login_required
def getalltool(): 
    res = requests.get(const.PUBLIC_API + "/api/v2/managetool/getall")
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