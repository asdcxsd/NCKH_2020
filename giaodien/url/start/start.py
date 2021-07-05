from flask import Flask, render_template, request, session, jsonify, redirect, url_for,escape, Blueprint
from functools import wraps
Start = Blueprint('Start', __name__, template_folder='templates')
from .. import const
import requests

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
    account_id = session['user_id']
    param = {
        "account_id": account_id
    }
    res = requests.post(const.PUBLIC_API +"/api/v2/module/getaccountconfig", data=param)
    return res.json()