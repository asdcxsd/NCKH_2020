from flask import Flask, render_template, request, session, jsonify, redirect, url_for,escape, Blueprint
from functools import wraps
Start = Blueprint('Start', __name__, template_folder='templates')

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

@Start.route('/start')
@login_required
def start(): 
    return render_template('start.html')