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

Profile = Blueprint('Profile', __name__)

@Profile.route("/profile", methods=['GET'])
@login_required
def profile(): 
    return render_template("profile.html")

@Profile.route("/changepassword", methods=['POST'])
@login_required
def change_password_request(): 
    if "currentPassword" in request.form: 
        currentpassword = request.form['currentPassword']
    if "NewPassword" in request.form: 
        newpassword = request.form['NewPassword']
    if "confirmPassword" in request.form: 
        confirmPassword = request.form['confirmPassword']
    if newpassword!= confirmPassword: 
        data_for_return = {
            "message": "success", 
            "data": "confirm password mismatch"
        }
        return jsonify(data_for_return)
    data = {
        "Account_id": session['user_id'],
        "currentpassword": currentpassword, 
        "newpassword": newpassword
    }
    res = requests.post(const.PUBLIC_API + "/api/v2/module/changepassword", data = data)
    return res.json()