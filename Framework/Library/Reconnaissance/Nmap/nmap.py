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
from Framework.Library.Reconnaissance.Nmap.output import ModuleOutput
from Framework.Library.Reconnaissance.Nmap.input import ModuleInput
from Framework.Library.Reconnaissance.Nmap.analysis import analysis_service



class ModuleFramework(Module):
    name = "Nmap"
    type_module = "Module_Reconnaissance"
    path_input_class = "/input.py"
    path_output_class = "/output.py"
    ans = []
    url = ''
    filename = 'nmap.py'
    path_log = ""
    input_module = None
    status = ''
    result_of_other_tool = {}
    list_tool_run = []
    #docker 
    docker_name  = "instrumentisto/nmap:7.92"
    container = None

    def __init__(self):
        self.status = ValueStatus.Creating
        
    def info(self):
        result = {}
        result['name'] = self.name
        result['typemodule'] = self.type_module
        result['type'] = "offline"
        result['version'] = '2.0'
        return result

    def __del__(self):
        try:
            if self.container != None: 
                if self.container.remove_containers():
                    print("Remove Container OK")
                self.delete_path_log();
        except Exception as e:
            print("Error remove nmap", e)

    def start(self):
        if self.status != ValueStatus.Creating:
            return False
        print("Start" , self.name)
        self.status = ValueStatus.Running
        inputurl = self.get_input_for_running()
        if inputurl == False:
            self.status = ValueStatus.Error
            return
        try:
            self.container = ContainersDocker(self.docker_name)
            self.make_path_log();
            volumes = {self.path_log: {"bind": "/tmp/" , "mode":"rw"}}
            command = " -O -sV -Pn -vv  -p1-65535 " + inputurl + " --open -oX  /tmp/nmap.xml"
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
            print("Error run process", self.name, ":", e)
            self.status = ValueStatus.Error
    def is_running(self, result= ''):
        try:
            
            status = self.container.containers_status()
            if status == False: return False
            return  ContainerStatus.Running == status or ContainerStatus.Restarting == status
        except Exception as e:
            return False
    def convert_answer_to_object_output(self):
        if self.is_running():
            return "Process running"
        try:
            import time
            time.sleep(3)
            self.output_module  = ModuleOutput()
            self.output_module.RECON_PORTS = []
            with open(self.path_log  +  "nmap.xml") as file:
                data = file.read()
                #ss
                data_json_url = xmltodict.parse(data)
                file.close()
            try:
                ports = data_json_url['nmaprun']['host']['ports']['port']
                if not isinstance(ports, list):
                    ports = [ports]
                for port in ports:
                    try:
                        # add port 
                        self.output_module.RECON_PORTS.append(int(port['@portid']))
                        #add service
                        service_json = analysis_service(port)
                        self.output_module.RECON_SERVICES.append(service_json)
                    except:
                        pass
            except Exception as e:
                print("Nmap read data -> no port", e)
            try:
                osmatchs = data_json_url['nmaprun']['host']['os']['osmatch']
                if not isinstance(osmatchs, list):
                    osmatchs = [osmatchs]
                for osmatch in osmatchs:
                    try:
                        # add port 
                        self.output_module.RECON_OS.append(osmatch['osclass']['@osfamily'].lower())
                        #add service
                        #service_json = analysis_service(port)
                        #self.output_module.RECON_SERVICES.append(service_json)
                    except:
                        pass
            except Exception as e:
                print("Nmap read data -> no os", e)
        except Exception as e:
            print("Exception error parse json output nmap", str(e))
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
            print("Error get input for Nmap", e)
    def get_output_module(self):
        return self.output_module
    def add_data_to_object_output(self, inputObjectTarget, outputObject):


        return outputObject

    def get_input_for_running(self):
        result = False
        data = self.input_module
        if len(data.IN_IP) > 0: 
            result = data.IN_IP[0]
        if len(data.IN_DOMAIN)> 0 and result == "":
            result = data.IN_DOMAIN[0]
        
        return result


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