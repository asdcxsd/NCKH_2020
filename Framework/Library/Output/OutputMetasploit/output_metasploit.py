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
import os, time, requests, json

from subprocess import Popen, PIPE, STDOUT

from Framework.Library.Module import Module
from Framework.Library.Output.OutputMetasploit.output import ModuleOutput
from Framework.Library.Output.OutputMetasploit.input import ModuleInput


class ModuleFramework(Module):
    name = "OutputMetasploit"
    type_module = "Module_Output"
    path_input_class = "/input.py"
    path_output_class = "/output.py"
    ans = []
    url = ''
    filename = 'output_metasploit.py'
    path_log = ""
    input_module = None
    config_module = None
    status = ''
    result_of_other_tool = {}
    Cf_Server_OpenPort = ""

    def __init__(self):
        self.status = ValueStatus.Creating
    def info(self):
        result = {}
        result['name'] = self.name
        result['typemodule'] = self.type_module
        result['type'] = "offline"
        result['version'] = "1.0"
        return result

    def start(self):
        # run 
        self.output_module = ModuleOutput()
        
        self.status = ValueStatus.Running
        try:
            self.Cf_Server_OpenPort = self.config_module['Cf_Server_Metasploit_OpenPort']
            Cf_PublicIP = self.config_module['Cf_PublicIP']
            Cf_PublicPort  = self.config_module['Cf_PublicPort']
            if (Cf_PublicPort == "Auto"):
                self.config_module['Cf_PublicPort'] = randint(7000,8000);
                Cf_PublicPort = self.config_module['Cf_PublicPort']
            self.output_module.make_config_connect(server_rev=self.Cf_Server_OpenPort, port_rev=Cf_PublicPort, ip_rev=Cf_PublicIP)
            dataout = self.input_module.to_json()['EXPLOIT_METASPLOIT_AI'][0]
            dataout['LHOST'] = Cf_PublicIP
            dataout['LPORT'] = Cf_PublicPort
            self.target_connect = dataout['ip_addr']
            datasend = {
                "inputdata" : json.dumps(dataout)
            }
            resultScan = self.request_to_server_metasploit_ai(datasend, "POST", "/openConnection")
            if resultScan != False and  resultScan['job_id'] !=None: 
                id_connect = str(resultScan['job_id'])
                self.output_module.update_status(self.target_connect, ValueStatus.Success, id_connect)
            else:
                self.output_module.update_status(self.target_connect,  ValueStatus.Error)
            self.status = ValueStatus.Success
        except Exception as e:
            print("Exception: ", self.name, e)
            self.status = ValueStatus.Error
            self.output_module.update_status("", ValueStatus.Error)
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


    def request_to_server_metasploit_ai(self, data, method, link):
        url = self.Cf_Server_OpenPort  + link
        header = {
            #"Content-type" : "application/x-www-form-urlencoded"
        }

        data =  data
        param =  data

        if method == "GET" : 
            data = {}
            header = {}
        else: 
            param = {}
        try:
            req = requests.request(method=method, url=url, data =data,params=param, headers= header )
            if  req.status_code  == 200:
                try:
                    data_json = json.loads(req.text)
                    return data_json
                except:
                    pass
        except Exception as e:
            print("Connect server error: ", self.Cf_Server_OpenPort, )
        return False



if __name__ == "__main__": 
      
    pass