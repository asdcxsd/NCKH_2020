from Framework.Framework import Framework
from api.v1.output import make_output
from flask import request, Blueprint, Response
from Application.Function.Connect_Framework import get_class_module
from Application.run import RunFrammework
import os
from configvalue import UPLOAD_FOLDER_TOOLS
ToolManager = Blueprint("ToolManager", __name__)

import threading
import time
import wget
import json
exporting_threads = {}

class ExportingThread(threading.Thread):
    def __init__(self, url,  save_path):
        self.progress = 0
        self.save_path = save_path
        self.url = url
        super().__init__()
    def bar_progress(self, current, total, width=80):
       progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
       self.progress = current/total * 100
    
    def run(self): 
        wget.download(self.url, self.save_path, bar = self.bar_progress)


@ToolManager.route("/update", methods=['POST'])
def update_tool_to_server(): 
    try: 

        if "list_tool" in request.form: 
            list_tool_update = request.form.getlist("list_tool")
        if "update_server" in request.form: 
            update_server = request.form['update_server']
        if "list_tool_delete" in request.form: 
            list_tool_delete = request.form.getlist("list_tool_delete")
            if len(list_tool_delete): 
                for tool_filename in list_tool_delete: 
                    tool_path = UPLOAD_FOLDER_TOOLS + tool_filename
                    os.remove(tool_path)
        for i in range(len(list_tool_update)): 
            save_path = UPLOAD_FOLDER_TOOLS + list_tool_update[i]
            url = update_server + "/tool/download/" + list_tool_update[i]
            global exporting_threads
            exporting_threads[i] = ExportingThread(url, save_path)
            exporting_threads[i].start()
        return Response(make_output(data="starting update tool", message='success'), mimetype="application/json", status=200)
    except Exception as e: 
        print(e)
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)

@ToolManager.route("/progress/<int:sum_thread>", methods=['GET'])
def progress_update_tool(sum_thread): 
    try: 
        global exporting_threads
        sum_thread_percentage = 0
        for i in range(sum_thread): 
            sum_thread_percentage += int(exporting_threads[i].progress/sum_thread)
        return Response(make_output(data=sum_thread_percentage, message="success"), mimetype="application/json", status=200)
    except Exception as e:
        print(e)
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)


        



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
        print(tool_path)
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
        

