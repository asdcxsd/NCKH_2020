from Framework.Framework import Framework
from api.v1.output import make_output
from flask import request, Blueprint, Response
from Application.Function.Connect_Framework import get_class_module
from Application.run import RunFrammework
import os
from configvalue import UPLOAD_FOLDER_TOOLS
ToolManager = Blueprint("ToolManager", __name__)

@ToolManager.route('/getall', methods=['POST'])
def get_all_tool(): 
    try: 
        if "module_name" in request.form: 
            module_name = request.form['module_name']
            result = []
            if module_name == "all": 
                framework = Framework()
                List_all_tool_recon = framework.get_list_of_module("Module_Reconnaissance")
                list_all_tool_exploit = framework.get_list_of_module("Module_Exploit")
                for i in List_all_tool_recon: 
                    result.append(framework.get_info_main_module(i))
                for i in list_all_tool_exploit: 
                    result.append(framework.get_info_main_module(i))
            else: 
                framework = Framework()
                List_all_tool = framework.get_list_of_module(module_name)
                for i in List_all_tool: 
                    result.append(framework.get_info_main_module(i))
            return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)



@ToolManager.route("/gettoolsdownloaded", methods=['GET'])
def get_all_tool_in_download_folder(): 
    try: 
        tool_path = UPLOAD_FOLDER_TOOLS
        files = os.listdir(tool_path)
        result = []
        for file in files: 
            filename = file.replace(".zip", "")
            temp = {}
            temp['toolname'] = filename.split('v')[0]
            temp['toolversion'] = filename.split('v')[1]
            temp['tool_filename'] = file
            result.append(temp)
        return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
    except Exception as e: 
        return Response(make_output(data=str(e), message='fail'), mimetype="application/json", status=404)



@ToolManager.route("/import", methods=['POST'])
def import_tools():
    try:
        filename = request.form['filename']
        frmWork = RunFrammework()
        status = frmWork.import_tool(filename)
        if status: 
            return Response(make_output(data="Import success!", message="success"), mimetype="application/json", status=200)
        else: 
            raise Exception("Import tool error")

    except Exception as e: 
        return Response(make_output(data=str(e), message="success"), mimetype="application/json", status=404)
        

@ToolManager.route("/remove", methods=['POST'])
def remove_tools():
    try:
        filename = request.form['filename']
        frmWork = RunFrammework()
        status = frmWork.remove_tool(filename)
        if status: 
            return Response(make_output(data="Remove success!", message="success"), mimetype="application/json", status=200)
        else: 
            raise Exception("Remove tool error")

    except Exception as e: 
        return Response(make_output(data=str(e), message="success"), mimetype="application/json", status=404)
        

