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
from concurrent.futures import ThreadPoolExecutor
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
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
        result['version'] = "2.0"
        return result

    def start(self):
        self.check_status_running_other_tools()
        if self.status != ValueStatus.Watting:
            return False
        print("Start" , self.name)
        self.status = ValueStatus.Running
        self.result = []
        try:
            try:
                self.input_module.RECON_PORTS.extend([80, 443])
                self.input_module.RECON_PORTS.extend(self.result_of_other_tool.Data['Module_Reconnaissance']['RECON_PORTS'])
            except:
                pass
            self.input_module.remove_duplicate()
            data = self.input_module.RECON_PORTS
            self.result = self.check_web_port(self.input_module.IN_IP[0], data)
            if self.status == ValueStatus.Stopping:
                self.status = ValueStatus.Error
                return
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
            list_data = []
            for data_inp in input.values():
                list_data.append(data_inp)

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
            if self.status == ValueStatus.Stopping:
                return
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
    
    def check_web_only_port(self,target_url,http):
        

            try:
                

                res = http.request('GET', target_url, retries=False)
                # self.print_message(OK, 'Port "{}" is web port. status={}'.format(port_num, res.status))
                self.web_port_list.append(target_url)
            except Exception as e:
                pass
                #self.print_message(WARNING, 'Port "{}" is not web port.'.format(port_num))
                # raise Exception(str(port_num)+ ' is not web port')
    def check_web_port(self, target_ip, port_list):
        #self.print_message(NOTE, 'Check web port.')
        self.web_port_list = []

        connection_pg = urllib3.PoolManager(maxsize=5, timeout=2)
        thread_pool = ThreadPoolExecutor(5)
        for port_num in port_list:
            for scheme in ['http://', 'https://']:
                if self.status == ValueStatus.Stopping:
                    break
                from time import sleep
                sleep(0.5)
                target_url = scheme + target_ip + ':' + str(port_num)
                thread_pool.submit(self.check_web_only_port, target_url, connection_pg)
        thread_pool.shutdown()
        return self.web_port_list
if __name__ == "__main__":    pass