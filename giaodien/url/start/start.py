from flask import Flask, render_template, request, session, jsonify, redirect, url_for,escape, Blueprint
from functools import wraps

from flask.wrappers import Response
Start = Blueprint('Start', __name__, template_folder='templates')
from .. import const
import requests


def GetConfigData(): 
    if session['config_id'] != '': 
        return [True, session['config_id']]
    else: 
        return [False, "Chưa cấu hình config"]
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

@Start.route('/start', methods=['GET'])
@login_required
def start(): 
    return render_template('start.html')

@Start.route('/getconfigdata', methods=['GET'])
@login_required
def get_config_data(): 
    status, data = GetConfigData(); 
    result = {
        "data": data, 
        "message": status
    }
    return result
