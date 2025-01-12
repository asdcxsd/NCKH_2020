from flask import Flask, render_template, request, session, jsonify, redirect, url_for,escape, Blueprint, session
from functools import wraps

from flask.wrappers import Response
from .. import const
import requests
import json

Login = Blueprint('Login', __name__, template_folder='templates')



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

@Login.route('/login', methods=['POST'])
def login():
    if not ('username' in request.form and 'password' in request.form): 
        return jsonify({'is_authenticated': False, 'msg': "Hãy nhập đầy đủ thông tin"})
    username = escape(request.form.get('username').strip())
    password = escape(request.form.get('password'))
    if not len(username) or not len(password): 
        return jsonify({'is_authenticated': False, 'msg': 'Tên đăng nhập hoặc mật khẩu bị thiếu'})
    param = {
        "username": username, 
        "password": password
    }
    res = requests.post(const.PUBLIC_API + "/api/v2/module/login", data=param)
    resp = res.json()
    if(resp['message'] == "Login Success"): 
        session['logged_in'] = True 
        session['user_id'] = resp['data']['_id']
        session["role"] = resp['data']['role']
        param = {
            "account_id": session['user_id']
        }
        res = requests.post(const.PUBLIC_API +"/api/v2/module/getaccountconfig", data=param)
        result = res.json()
        if(result['message'] == 'success'): 
            session['config_id'] = result['data']['$oid']
        else: 
            session['config_id'] = ''
        
        session['username'] = username.title()
        return jsonify({'is_authenticated': True, 'msg': ''})
    else: 
        return jsonify({'is_authenticated': False, 'msg': 'Tên đăng nhập hoặc mật khẩu không đúng'})



@Login.route("/getusername", methods=['GET'])
@login_required
def get_username_request(): 
    try: 
        username = session['username']
        data_for_return = {
            "data": username, 
            "message": "success"
        }
        return jsonify(data_for_return)

    except Exception as e: 
        data_for_return = {
            "data": str(e), 
            "message": "fail"
        }
        return jsonify(data_for_return)

@Login.route('/login',methods=['GET'])
def login1(): 
    
    if not 'logged_in' in session: 
        return render_template('login.html')
    if session['logged_in']: 
        
        return redirect(url_for('Login.index'))

@Login.route('/logout', methods=['GET'])
@login_required
def logout():
    session.clear()
    return render_template("login.html")
   


@Login.route('/', methods=['GET'])
@Login.route('/index', methods=['GET'])
@login_required
def index(): 
    return render_template('dashboard.html')