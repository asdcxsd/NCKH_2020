from flask import Flask, render_template, request, session, jsonify, redirect, url_for,escape, Blueprint
from functools import wraps
from flask.helpers import make_response

from flask.wrappers import Response
from .. import const
import requests
from url.login.login import Login, login
import json

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

Target = Blueprint('Target', __name__)

@Target.route('/target',methods=['GET'])
@login_required
def target(): 
    return render_template('target.html')

@Target.route('/addtarget', methods=['POST'])
@login_required
def addtarget(): 
    param = {}
    authen = {}
    if "targetname" in request.form: 
        param["name"] = request.form['targetname']
    if "targetIP" in request.form: 
        param['ip_address'] = request.form["targetIP"]
    if "targetDomain" in request.form: 
        param['domain'] = request.form['targetDomain']
    if "targetdescription" in request.form: 
            param['describe'] = request.form['targetdescription']
    if "username" in request.form: 
        authen['username'] = request.form['username']
    if "password" in request.form: 
        authen['password'] = request.form['password']
    if dict(authen): 
        param['authen'] = json.dumps(authen)
    res = requests.post(const.PUBLIC_API + "/api/v2/target/insert", data=param)
    return res.json()

@Target.route('/getalltarget', methods=['GET'])
@login_required
def getalltarget(): 
    res = requests.get(const.PUBLIC_API + "/api/v2/target/getall")
    return res.json()

@Target.route("/deletetarget", methods=['DELETE'])
@login_required
def deletetarget(): 
    targetid = request.form['targetid']
    param = {
        'target_id': targetid
    }
    res = requests.delete(const.PUBLIC_API + "/api/v2/target/delete", data=param)
    return res.json()

@Target.route("/gettarget", methods=['POST'])
@login_required
def gettarget(): 
    target_id = request.form['id']
    param = {
        "target_id": target_id
    }
    res = requests.get(const.PUBLIC_API + '/api/v2/target/gettarget', params=param)
    return res.json()

@Target.route('/updatetarget', methods=['POST'])
@login_required
def update_target(): 
    param = {}
    if "targetid" in request.form: 
        param['target_id'] = request.form['targetid']
    if "targetName" in request.form: 
        param['name'] = request.form['targetName']
    if "targetIP" in request.form: 
        param['ip_address'] = request.form['targetIP']
    if "targetDomain" in request.form: 
        param['domain'] = request.form['targetDomain']
    if "targetDescription" in request.form: 
        param['describe'] = request.form['targetDescription']
    if "username" in request.form and "password" in request.form: 
        authen = {}
        authen['username'] = request.form['username']
        authen['password'] = request.form['password']
        param['authen'] = json.dumps(authen)
    res = requests.post(const.PUBLIC_API + "/api/v2/target/update", data=param)
    return res.json()
