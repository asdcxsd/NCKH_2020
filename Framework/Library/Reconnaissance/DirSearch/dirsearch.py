#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Framework.Valueconfig import ValueStatus
from ...manager_docker import ContainersDocker
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

from Framework.Library.Module import Module
from .input import ModuleInput
from .output import ModuleOutput



class ModuleFramework(Module):
    name = "DirSearch"
    type_module = "Module_Reconnaissance"
    path_input_class = "/input.py"
    path_output_class = "/output.py"
    ans = []
    urls = []
    filename = 'dirsearch.py'
    path_log = ""
    process = []
    answer = []
    input_module = None
    input_data = []
    status = ''

    #docker 
    docker_name  = "dirsearch:v0.4.1"
    containers = []

    def __init__(self):
        self.status = ValueStatus.Creating
        
    def info(self):
        result = {}
        result['name'] = self.name
        result['typemodule'] = self.type_module
        result['type'] = "offline"
        return result

    def __del__(self):
        try:
            if self.containers != []: 
                for container in self.containers:
                    if container.remove_containers():
                        print("Remove Container OK")
                self.delete_path_log();
        except Exception as e:
            print(e)

    def start(self):
        self.check_status_running_other_tools()
        if self.status != ValueStatus.Creating:
            return False
        self.status = ValueStatus.Running
        data = self.result_of_other_tool.Data['Module_Reconnaissance']
        self.urls =  data['RECON_WEBAPP']
        from hashlib import md5
        m = hashlib.md5()
        #inputurl = self.get_input_for_running()
        for url in self.urls:
            try:
                m.update((url))
                md5string=m.digest()
                self.containers.append(ContainersDocker(self.docker_name))
                self.make_path_log();
                volumes = {self.path_log: {"bind": "/tmp/" , "mode":"rw"}}
                command = "-u " + url + "  --json-report=/tmp/dirsearch_"+md5string+".json"
                self.containers[-1].run_containers_cmd(volumes=volumes, command=command, detach=True  )
            except Exception as e:
                print("Error run process:", e)
        return 0
    def getstatus(self, result= ''):
        try:
            #True -> running
            #False -> stop
            for container in  self.containers:
                status = container.containers_status()
                if status == False: return False
                if "running" == status or "created" == status:
                    return False
            return True
        except Exception as e:
            return False
    def getanswer(self):
        if self.getstatus():
            return "Process running"
        self.answer = {}
        from hashlib import md5
        m = hashlib.md5()
        self.answer["RECON_DIR"] = []
        self.answer["RECON_FILE"] = []
        for url in self.urls:
            list_result = []
            m.update((url))
            md5string=m.digest()
            try:
                with open(self.path_log  +  "dirsearch"+ md5string+".json") as file:
                    data_json_url = json.loads(file.read())
                    file.close()
            except Exception as e:
                print(e)
                self.answer["RECON_DIR"].append(self.url)
                return self.answer
        if url not in self.answer["RECON_DIR"] : 
            self.answer["RECON_DIR"].append(self.url)
        for key, val in data_json_url.items():
            if key == "time":
                continue
            self.answer["RECON_DIR"].append(key)
            key_path = key[:-1]
            for path in val:
                try:
                    if (path['status'] >= 300 and path['status']  < 400) :
                        self.answer["RECON_DIR"].append(key_path + path['path'] + "/")
                    if path['status'] == 403 and path['path'][-1] == '/':
                        self.answer["RECON_DIR"].append(key_path + path['path'])
                    if path['status'] <300: 
                        self.answer["RECON_FILE"].append(key_path + path['path'])
                    if  path['status'] >= 500 and  path['content-length'] > 0:
                        self.answer["RECON_FILE"].append(key_path + path['path'])
                    
                        
                except Exception as e: 
                    print("Error with path: ", e)
        
        return self.answer
       
        return self.answer

    def get_status(self):
        return self.status
    def set_input_module(self, input):
        self.input_data = input
    def get_output_module(self):
        return self.output_module
        
    def add_data_to_object_output(self, inputObjectTarget, outputObject):


        return outputObject

    def get_input_for_running(self):
        data =  self.input_data
        output = ""

            

    def make_path_log(self): 
        if self.path_log != '':
            return
        self.path_log =  'temp/'
        self.path_log +=  ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) +  str(datetime.datetime.now().timestamp()).split('.')[0] +'/'
        if not os.path.exists(self.path_log):
            os.mkdir(self.path_log)
   
    def delete_path_log(self):
        try:
            print("Remove Log" + self.path_log)
            shutil.rmtree(self.path_log)
        except Exception as e:
            print(str(e))

    def check_status_running_other_tools(self):
        list_check = ['Nmap', "WebAppDetect"]
       
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

       

if __name__ == "__main__": 
      
    pass