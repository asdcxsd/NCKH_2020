from types import MethodDescriptorType
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

Input = Blueprint('Input', __name__)
@Input.route("/input", methods=['GET'])
@login_required
def input(): 
    return render_template("input.html")

@Input.route("/getallinput", methods=['GET'])
@login_required
def get_all_input(): 
    res = requests.get(const.PUBLIC_API + "/api/v2/input/getall")
    return res.json()

@Input.route('/deleteinput', methods=['DELETE'])
@login_required
def delete_input_request(): 
    if 'input_id' in request.form: 
        param = {
            "input_id": request.form['input_id']
        }
        res = requests.delete(const.PUBLIC_API + "/api/v2/input/remove", data=param)
        return res.json()

@Input.route("/getinput", methods=['POST'])
@login_required
def get_input_detail_request(): 
    param = {}
    if "input_id" in request.form: 
        param['input_id'] = request.form['input_id']
    if "process_id" in request.form: 
        param['process_id'] = request.form['process_id']
    res = requests.post(const.PUBLIC_API + "/api/v2/input/detail", data=param)
    return res.json()