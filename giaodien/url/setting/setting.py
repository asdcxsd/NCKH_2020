from flask import Flask, render_template, request, session, jsonify, redirect, url_for,escape, Blueprint
from functools import wraps
Setting = Blueprint('Setting', __name__, template_folder='templates')


@Setting.route('/setting')
def setting(): 
    return render_template('setting.html')