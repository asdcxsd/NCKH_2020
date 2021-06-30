from flask import Flask, render_template, request, session, jsonify, redirect, url_for,escape, Blueprint
from functools import wraps
from .. import const
import requests
from url.login.login import Login

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
    targetname = request.form['targetname']
    targetdescription = request.form['targetdescription']
    param = {
        "url": targetname, 
        "name": targetdescription
    }
    res = requests.post(const.PUBLIC_API + "/api/v1/target/insert", data=param)
    return res.json()

@Target.route('/getalltarget', methods=['GET'])
@login_required
def getalltarget(): 
    res = requests.get(const.PUBLIC_API + "/api/v1/target/getall")
    return res.json()

@Target.route("/deletetarget", methods=['DELETE'])
@login_required
def deletetarget(): 
    targetid = request.form['targetid']
    param = {
        'target_id': targetid
    }
    res = requests.delete(const.PUBLIC_API + "/api/v1/target/delete", data=param)
    return res.json()

@Target.route("/gettarget", methods=['POST'])
@login_required
def gettarget(): 
    target_id = request.form['id']
    param = {
        "target_id": target_id
    }
    res = requests.get(const.PUBLIC_API + '/api/v1/target/gettarget', params=param)
    return res.json()
