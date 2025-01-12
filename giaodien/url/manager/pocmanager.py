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


def admin_required(func): 
    @wraps(func)
    def wrapper(*args, **kwargs): 
        if session['role'] and session['role'] != "admin": 
            return redirect(url_for('POCManager.forbiden'))
        else: 
            return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
    
POCManager = Blueprint('POCManager', __name__)


@POCManager.route('/403', methods=['GET'])
@login_required
def forbiden(): 
    return render_template('403.html')


@POCManager.route('/quanlipoc', methods=['GET'])
@login_required
@admin_required
def pocmanager(): 
    return render_template('quanlyPOC.html')

@POCManager.route("/fetchpocs", methods=['GET'])
@login_required
@admin_required
def fetchpoc(): 
    res = requests.get(const.PUBLIC_API + "/api/v2/managepoc/getall")
    
    return res.json()

@POCManager.route('/removepoc', methods=['DELETE'])
@login_required
@admin_required
def removepoc(): 
    try: 
        pocname = request.form['pocname']
        data = {
            'filename': pocname
        }
        res = requests.delete(const.PUBLIC_API +"/api/v2/managepoc/remove", data=data)
        
        return res.json()
    except Exception as e: 
        
        return e


@POCManager.route('/detailpoc', methods=['GET'])
@login_required
@admin_required
def detailpoc(): 
    pocname = request.args['poc_name']
    param = {
        "poc_name": pocname
    }
    res = requests.post(const.PUBLIC_API + "/api/v2/managepoc/getdetail", data=param)
    return res.json()


@POCManager.route("/uploadpoc", methods=['POST'])
@login_required
@admin_required
def UploadPoc(): 
    Files = request.files.get('file')
    filename = Files.filename
    Files_bytes = Files.read()
    files = {
        "file": (filename, Files_bytes)   
    }
    headers={'Content-Type': 'multipart/form-data'}
    res = requests.post(const.PUBLIC_API + "/api/v2/managepoc/uploadpoc",files=files)
    return res.json()


