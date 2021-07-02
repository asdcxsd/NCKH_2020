from flask import Flask, render_template, request, session, jsonify, redirect, url_for,escape, Blueprint
from functools import wraps
from lib import database
Login = Blueprint('Login', __name__, template_folder='templates')
db = database.Database()


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
    
    if (db.authenticate(username, password) == None): 
        return jsonify({'is_authenticated': False, 'msg': 'Tên đăng nhập hoặc mật khẩu không đúng'})
    user_id, role = db.authenticate(username, password)
    session['logged_in'] = True 
    session['user_id'] = user_id
    session['role'] = role
    session['username'] = username.title()
    return jsonify({'is_authenticated': True, 'msg': ''})

@Login.route('/login',methods=['GET'])
def login1(): 
    if not 'logged_in' in session: 
        return render_template('login.html')
    if session['logged_in']: 
        return redirect(url_for('Login.index'))

@Login.route('/logout')
@login_required
def logout():
    return 'logout'

@Login.route('/', methods=['GET'])
@Login.route('/index', methods=['GET'])
@login_required
def index(): 
    return render_template('dashboard.html')