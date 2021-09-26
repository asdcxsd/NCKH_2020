from flask import Flask, render_template, request, session, jsonify, redirect, url_for,escape, Blueprint
from functools import wraps
import requests
from .. import const
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

ToolManager = Blueprint('ToolManager', __name__)

@ToolManager.route('/quanlicongcu', methods=['GET'])
@login_required
def toolmanager(): 
    return render_template('quanlycongcu.html')

@ToolManager.route('/getalltool',methods=['POST'])
@login_required
def getalltool(): 
    if "module_name" in request.form: 
        module_name = request.form['module_name']
    param = {
        "module_name": module_name
    }
    res = requests.post(const.PUBLIC_API + "/api/v2/managetool/getall", data=param)
    
    return res.json()


@ToolManager.route("/gettoolsdownloaded", methods=['GET'])
@login_required
def update_tool(): 
    res = requests.get(const.PUBLIC_API + "/api/v2/managetool/gettoolsdownloaded")
    return res.json()

@ToolManager.route("/importtool", methods=['POST'])
@login_required
def import_tool(): 
    param = {
        "module_name": "all"
    }
    res = requests.post(const.PUBLIC_API + "/api/v2/managetool/getall", data=param)
    result = res.json()
    if "tool_filename" in request.form: 
        tool_import = request.form['tool_filename']
        tool_name = tool_import.replace('.zip',"").split("v")[0]
        tool_version = tool_import.replace('.zip',"").split("v")[1]
    if result['message'] == "success": 
        list_tool = result['data']
        flag = 0
        for tool in list_tool: 
            if tool['name'] == tool_name: 
                flag = 1
                if tool['version'] < tool_version: 
                    filename = {
                        "filename": tool_import
                    }
                    resp = requests.post(const.PUBLIC_API + "/api/v2/managetool/import", data=filename)
                    return resp.json()
                else: 
                    data = {
                        "message": "fail", 
                        "data": "can not import tool"
                    }
                    return jsonify(data)
        if flag == 0: 
            filename = {
                "filename": tool_import
            }
            resp = requests.post(const.PUBLIC_API + "/api/v2/managetool/import", data=filename)
            return resp.json()




@ToolManager.route("/checktoolforupdate", methods=['GET'])
@login_required
def check_tool_for_update_on_system(): 
    res0 = requests.get(const.PUBLIC_API + "/api/v2/managetool/gettoolsdownloaded")
    temp = res0.json()
    list_tool_downloaded = []
    if temp['message'] == 'success': 
        list_tool_downloaded = temp['data']
    res1 = requests.get(const.UPDATE_SERVER + "/listtoolupdate")
    temp = res1.json()
    list_tool_update = []
    list_tool_need_download = []
    if temp['message'] == 'success': 
        list_tool_update = temp['data']
    for tool_update in list_tool_update: 
        if tool_update not in list_tool_downloaded: 
            list_tool_need_download.append(tool_update)
    data_for_return = {
        "message": "success", 
        "data" : list_tool_need_download
    }
    return jsonify(data_for_return)

        



@ToolManager.route('/deletetool', methods=['DELETE'])
@login_required
def deletetool(): 
    toolname = request.form['tool']
    data = {
        "filename": toolname
    }
    res = requests.post(const.PUBLIC_API + "/api/v2/managetool/remove", data=data)
    return res.json()