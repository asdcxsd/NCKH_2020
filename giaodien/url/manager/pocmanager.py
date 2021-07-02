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
POCManager = Blueprint('POCManager', __name__)

@POCManager.route('/quanlipoc', methods=['GET'])
@login_required
def pocmanager(): 
    return render_template('quanlyPOC.html')

@POCManager.route("/fetchpocs", methods=['GET'])
@login_required
def fetchpoc(): 
    res = requests.get(const.PUBLIC_API + "/api/v1/pocs/info_poc")
    return res.json()

@POCManager.route('/removepoc', methods=['DELETE'])
@login_required
def removepoc(): 
    pocname = request.form['pocname']
    data = {
        'namepoc': pocname
    }
    res = requests.delete(const.PUBLIC_API +"/api/v1/pocs/removepoc", data=data)
    return res.json()

@POCManager.route('/detailpoc', methods=['GET'])
@login_required
def detailpoc(): 
    pocname = request.args['pocname']
    param = {
        "namepoc": pocname
    }
    res = requests.get(const.PUBLIC_API + "/api/v1/pocs/detail_poc?", params=param)
    return res.json()


