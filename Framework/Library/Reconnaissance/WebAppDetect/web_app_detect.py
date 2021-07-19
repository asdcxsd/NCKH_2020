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
import os, urllib3
from Framework.Library.Module import Module
from Framework.Library.Reconnaissance.WebAppDetect.output import ModuleOutput
from Framework.Library.Reconnaissance.WebAppDetect.input import ModuleInput



class ModuleFramework(Module):
    name = "WebAppDetect"
    type_module = "Module_Reconnaissance"
    path_input_class = "/input.py"
    path_output_class = "/output.py"
    ans = []
    url = ''
    filename = 'web_app_detect.py'
    path_log = ""
    input_module = None
    status = ''
    result_of_other_tool = {}
    list_tool_run = []
    #docker 
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
        self.status = ValueStatus.Running
        self.result = []
        try:
            data = self.result_of_other_tool.Data['Module_Reconnaissance']
            self.result = self.check_web_port(self.input_module.IN_IP[0], data['RECON_PORTS'])
                   
            self.convert_answer_to_object_output()
            self.status = ValueStatus.Success
        except Exception as e:
            print("Error run process:", e)
            self.status = ValueStatus.Error
    
    def convert_answer_to_object_output(self):

        try:
            self.output_module  = ModuleOutput()
            self.output_module.RECON_WEBAPP = self.result
            
        except Exception as e:
            print("Exception error parse json output ", self.name, str(e))
            raise Exception(e)
    def get_status(self):
        return self.status
    def set_input_module(self, input):
        try:
            self.input_module = ModuleInput()
            list_data = input['Module_Input']
            if not isinstance(list_data, list):
                list_data = [list_data]

            for data in list_data:
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
        list_check = ['Nmap']
       
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
    def check_web_port(self, target_ip, port_list):
        #self.print_message(NOTE, 'Check web port.')
        web_port_list = []
        for port_num in port_list:
            # Send HTTP request.
            http = urllib3.PoolManager(timeout=1)
            for scheme in ['http://', 'https://']:

                try:
                    target_url = scheme + target_ip + ':' + str(port_num)
                
                    #client.keep_alive()
                    # self.print_message(OK, 'Target URL: {}'.format(target_url))
                    res = http.request('GET', target_url)
                    # self.print_message(OK, 'Port "{}" is web port. status={}'.format(port_num, res.status))
                    web_port_list.append(target_url)
                    break
                except Exception as e:
                    pass
                    #self.print_message(WARNING, 'Port "{}" is not web port.'.format(port_num))
                    # raise Exception(str(port_num)+ ' is not web port')
        return web_port_list
if __name__ == "__main__": 
      
    pass