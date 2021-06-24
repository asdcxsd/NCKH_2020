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
    path_input_class = "/input.py"
    path_output_class = "/output.py"
    ans = []
    url = ''
    filename = 'dirsearch.py'
    path_log = ""
    process = []
    answer = []
    input_module = None
    input_data = []
    status = ''

    #docker 
    docker_name  = "dirsearch:v0.4.1"
    container = None

    def __init__(self):
        self.status = ValueStatus.Creating
        
    def info(self):
        result = {}
        result['name'] = 'dirsearch'
        result['type'] = "offline"
        return result

    def __del__(self):
        try:
            if self.container != None: 
                if self.container.remove_containers():
                    print("Remove Container OK")
                self.delete_path_log();
        except Exception as e:
            print(e)

    def start(self):
        if self.status != ValueStatus.Creating:
            return False
        self.status = ValueStatus.Running
        inputurl = self.get_input_for_running()
        try:
            self.container = ContainersDocker(self.docker_name)
            self.make_path_log();
            volumes = {self.path_log: {"bind": "/tmp/" , "mode":"rw"}}
            command = "-u " + inputurl + "  --json-report=/tmp/dirsearch.json"
            self.container.run_containers_cmd(volumes=volumes, command=command, detach=True  )
        except Exception as e:
            print("Error run process:", e)
        return 0
    def getstatus(self, result= ''):
        try:
            status = self.container.contariners_status()
            if status == False: return False
            return  "running" == status or "created" == status
        except Exception as e:
            return False
    def getanswer(self):
        if self.getstatus():
            return "Process running"
        
       
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


       

if __name__ == "__main__": 
      
    pass