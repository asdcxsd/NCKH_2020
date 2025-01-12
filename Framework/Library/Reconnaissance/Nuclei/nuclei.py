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
from Framework.Library.Reconnaissance.Nuclei.output import ModuleOutput
from Framework.Library.Reconnaissance.Nuclei.input import ModuleInput
from Framework.Library.Function.MergeData.url_duplicate import MergeData as MergeDataURL


class ModuleFramework(Module):
    name = "Nuclei"
    type_module = "Module_Reconnaissance"
    path_input_class = "/input.py"
    path_output_class = "/output.py"
    ans = []
    url = ''
    filename = 'nuclei.py'
    path_log = ""
    input_module = None
    status = ''
    result_of_other_tool = {}
    list_tool_run = []
    result_input_service = []
    #docker 
    docker_name  = "projectdiscovery/nuclei"
    container = None
    list_service_nuclei = ['http', 'https', 'dns', 'file', 'tcp']
    def __init__(self):
        self.status = ValueStatus.Creating
        
    def info(self):
        result = {}
        result['name'] = self.name
        result['typemodule'] = self.type_module
        result['type'] = "offline"
        result['version'] = "2.0"
        return result
    def __del__(self):
        try:
            if self.container != None: 
                if self.container.remove_containers():
                    print("Remove Container OK")
                self.delete_path_log();
        except Exception as e:
            print("Error remove nuclei", e)
    def start(self):
        self.check_status_running_other_tools()
        if self.status != ValueStatus.Watting:
            return False
        print("Start" , self.name)
        self.status = ValueStatus.Running
        self.result_input_service = []
        try:
            services = self.input_module.RECON_SERVICES
            try:
                services.extend(self.result_of_other_tool.Data['Module_Reconnaissance']['RECON_SERVICES'])
            except :
                pass

            for service in services:
                if service['name'] not in self.list_service_nuclei:
                    continue
                service_name = service['name'] + "://" +  self.input_module.IN_IP[0] + ":" + str(service['port']) + "/"
                if service_name not in  self.result_input_service:
                    self.result_input_service.append(service_name)

            # add webapp
            webapps = self.input_module.RECON_WEBAPP
            try:
                webapps.extend(["http://" + self.input_module.IN_IP[0] + ":80","https://" + self.input_module.IN_IP[0] + ":443"])
                webapps.extend(self.result_of_other_tool.Data['Module_Reconnaissance']['RECON_WEBAPP'])
            except :
                pass

            self.result_input_service = MergeDataURL().merge_data(webapps, [])
            #check scan
            self.container = ContainersDocker(self.docker_name)
            self.make_path_log();
            with open(self.path_log + "input_target.txt", "w") as file_input:
                for service in self.result_input_service:
                    file_input.write(service + "\n")
                file_input.close()
            path_init = FOLDER_FRAMEWORK_ROOT + "Library/Reconnaissance/Nuclei/init_tools/nuclei-templates"
            
            volumes = {self.path_log: {"bind": "/tmp" , "mode":"rw"} , path_init : {"bind" : "/root/nuclei-templates", "mode" : "rw"}}
            command = " -l /tmp/input_target.txt -t /root/nuclei-templates/  --json -o /tmp/nuclei.json"
            #command =  " -h"
            self.container.run_containers_cmd(volumes=volumes, command=command, detach=True  )
            while self.is_running():
                import time 
                time.sleep(1)
                if self.status == ValueStatus.Stopping:
                    self.container.stop_containers()
                    self.status = ValueStatus.Error
                    return
            status = self.container.containers_status()
            print(self.name, status)
            self.convert_answer_to_object_output()
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
    def convert_answer_to_object_output(self):

        try:
            self.output_module  = ModuleOutput()
            try:

                data= open(self.path_log + "nuclei.json", "r").read()
                datajson = [json.loads(d) for d in data.split('\n')[:-1]]
                for data in datajson:
                    dataout = {}
                    dataout['name'] = data['info']['name']
                    dataout['host'] = data['host']
                    dataout['matched'] = data['matched']
                    dataout['ip'] = data['ip']
                    # get result 
                    dataout['results'] = []
                    if "extracted_results" in data:
                        dataout['results'].extend(data["extracted_results"])
                    if "meta" in data:
                        dataout['results'].append(data["meta"])
                    if "matcher_name" in data:
                        dataout['results'].append(data["matcher_name"])
                    insert = "NO"
                    for index, data_index in enumerate(self.output_module.RECON_CVE):
                        if data_index['name'] == dataout['name'] and (data_index['host'] ==  dataout['host'] or (data_index['matched'] == dataout['matched'] and data_index['ip'] == dataout['ip'] )):
                            self.output_module.RECON_CVE[index]['results'].extend(dataout['results'])
                            insert = "OK"
                    for index, data_index in enumerate(self.output_module.RECON_VULN):
                        if data_index['name'] == dataout['name'] and (data_index['host'] ==  dataout['host'] or (data_index['matched'] == dataout['matched'] and data_index['ip'] == dataout['ip'] )):
                            self.output_module.RECON_VULN[index]['results'].extend(dataout['results'])
                            insert = "OK"
                    #make trace

                    # make a  label
                    if insert == "NO":
                        if "detect" in data['templateID']:
                            self.output_module.add_recon_technology(dataout)
                        elif "CVE" in data['templateID']:
                            dataout['name'] = data['templateID']
                            self.output_module.RECON_CVE.append(dataout)
                        else:
                            self.output_module.RECON_VULN.append(dataout)
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
