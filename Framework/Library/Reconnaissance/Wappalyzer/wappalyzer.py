#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Framework.Valueconfig import ValueStatus, FOLDER_FRAMEWORK_ROOT
from Framework.Library.Function.manager_docker import ContainerStatus, ContainersDocker
import os
from datetime import date
import re
from sys import path
from urllib.parse import urlsplit
import hashlib
import os, datetime, binascii
import shutil, json
import random, string
from subprocess import Popen, PIPE, STDOUT
import xmltodict
from Framework.Library.Module import Module
from Framework.Library.Reconnaissance.Wappalyzer.output import ModuleOutput
from Framework.Library.Reconnaissance.Wappalyzer.input import ModuleInput



class ModuleFramework(Module):
    name = "Wappalyzer"
    type_module = "Module_Reconnaissance"
    path_input_class = "/input.py"
    path_output_class = "/output.py"
    ans = []
    url = ''
    filename = 'wappalyzer.py'
    path_log = ""
    input_module = None
    status = ''
    result_of_other_tool = {}
    list_tool_run = []
    result_input_service = []
    #docker 
    docker_name  = "wappalyzer/cli"
    container = None
    def __init__(self):
        self.status = ValueStatus.Creating
        
    def info(self):
        result = {}
        result['name'] = self.name
        result['typemodule'] = self.type_module
        result['type'] = "offline"
        return result
    def start(self):
        
        self.check_status_running_other_tools()
        if self.status != ValueStatus.Watting:
            return False
        print("Start" , self.name)
        self.output_module  = ModuleOutput()
        self.status = ValueStatus.Running
        self.result_input_service = []
        try:

            # add webapp
            webapps = self.input_module.RECON_WEBAPP
            try:
                webapps.extend(self.result_of_other_tool.Data['Module_Reconnaissance']['RECON_WEBAPP'])
            except :
                pass
            for webapp in webapps :
                 if webapp not in  self.result_input_service:
                        self.result_input_service.append(webapp)
            #check scan
            self.container = ContainersDocker(self.docker_name)
            for webapp in self.result_input_service:

                self.container.run_containers_cmd(command=webapp, detach=True)
                while self.is_running():
                    import time 
                    time.sleep(1)
                status, anstext  = self.container.get_comtainers_output()
                if status:
                    self.convert_answer_to_object_output(anstext)
            status = self.container.containers_status()
            print(self.name, status)
            self.status = ValueStatus.Success
        except Exception as e:
            print("Error run process:", e)
            self.status = ValueStatus.Error
    def is_running(self, result= ''):
        try:

            status = self.container.containers_status()
            if status == False: return False
            return  ContainerStatus.Running == status or ContainerStatus.Restarting == status
        except Exception as e:
            return False
    def convert_answer_to_object_output(self, anstext):

        try:
           
            try:
                datajson  = json.loads(anstext)

                self.output_module.add_recon_technology(datajson)
            except Exception as e:
                print("read error data", self.name, e)
        except Exception as e:
            print("Exception error parse json output ", self.name, str(e))
            raise Exception(e)
    def get_status(self):
        return self.status
    def set_input_module(self, input):
        try:
            self.input_module = ModuleInput()
            list_data_ans = []
            for list_data_index in input.values():

                list_data =  list_data_index
                if not isinstance(list_data_index, list):
                    list_data = [list_data_index]
                list_data_ans.extend(list_data)
            for data in list_data_ans:
                temp_module = ModuleInput()
                temp_module.try_parse(data)
                self.input_module.extend(temp_module)
        except Exception as e:
            print("Error get input for", self.name, e)
    def get_output_module(self):
        return self.output_module
    def add_data_to_object_output(self, inputObjectTarget, outputObject):


        return outputObject

    def check_status_running_other_tools(self):
        list_check = ['Nmap', 'WebAppDetect']
       
        while(True):
            ok = ValueStatus.Watting
            for id_tool in range(len(self.list_tools)):
                if not self.list_tools[id_tool] in list_check:
                    continue
                st_tool = self.list_status[id_tool]
                if st_tool == None:
                    continue
                if st_tool.getStatus() not in  [ValueStatus.Success, ValueStatus.Error] :
                    ok = ValueStatus.Loading
                    break
            if ok == ValueStatus.Watting:
                break
        self.status = ok

            
    def update_result_process_session(self, list_tools, list_status, list_result):
        self.list_tools = list_tools
        self.result_of_other_tool = list_result
        self.list_status = list_status
            #self.result_of_other_tool

    def make_path_log(self):
        if self.path_log != '':
            return
        self.path_log =  FOLDER_FRAMEWORK_ROOT + 'temp/'
        self.path_log +=  ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) +  str(datetime.datetime.now().timestamp()).split('.')[0] +'/'
        if not os.path.exists(self.path_log):
            os.mkdir(self.path_log)
   
    def delete_path_log(self):
        try:
            print("Remove Log" + self.path_log)
            shutil.rmtree(self.path_log)
        except Exception as e:
            print(str(e))
if __name__ == "__main__": 
      
    pass