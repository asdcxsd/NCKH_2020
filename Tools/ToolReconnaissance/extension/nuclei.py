#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Library.manager_docker import ContainersDocker
import os
from datetime import date
import re
from sys import flags, path
from urllib.parse import urlsplit
import hashlib
import os, datetime, binascii
import json
import shutil
import random, string
from threading import Thread
from configvalue import *
from subprocess import Popen, PIPE, STDOUT
import docker
import requests
class reconnaissance():
    ans = []
    path_log = ""
    name  = "nuclei-2"
    filename = 'nuclei.py'
    init_folder = 'init_tools_nuclei'
    process = None
    answer = []
    proc = ''
    url = ''
    have_dirseach = 'not run'
    classcalling = 0
    container = None
    def __init__(self, *args, **kwargs):
        self.have_dirseach = 'not run'
        if "run" in args:
            print("nuclie docker running")
        
    def info(self):
        result = {}
        result['name'] = 'nuclei'
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
    def make_path_log(self): 
        if self.path_log != '':
            return
        self.path_log = DICTIONLARY_HOME + 'temp/'
        self.path_log +=  ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) +  str(datetime.datetime.now().timestamp()).split('.')[0] +'/'
        if not os.path.exists(self.path_log):
            os.mkdir(self.path_log)
   
    def delete_path_log(self):
        try:
            print("Remove Log" + self.path_log)
            shutil.rmtree(self.path_log)
        except Exception as e:
            print(str(e))
    def run_nuclei(self, result):
        try:

            # save to file target 
            self.make_path_log();
            savefile = self.path_log + "input.txt"
            fileinput = open(savefile, 'wb');
            for dir  in result:
                fileinput.write((dir + "\n").encode())
            fileinput.close()
            self.container = ContainersDocker(self.name)
            
            path_init = FOLDER_TOOLS + "init_tools/" + self.init_folder + "/nuclei-templates"
            
            volumes = {self.path_log: {"bind": "/tmp" , "mode":"rw"}, path_init : {"bind" : "/root/nuclei-templates", "mode" : "rw"}}
            command = "-l /tmp/input.txt -t cves  -json -o /tmp/nuclei.json"
            self.container.run_containers_cmd(volumes=volumes, command=command, detach=True  )
        except Exception as e:
            print("Error run process:", e)  
    def run(self, inputurl):
        self.url = inputurl
        #if self.getstatus() == True:
        #   print("Process busy")
        return "Process busy"
        return 0
    def getstatus(self, result= '', getanswer = False):
        try:
            if result == '' and getanswer == False: 
                return True
            
            for x in result:
                if self.have_dirseach !='dirsearch end' and x.info()['name'] == 'dirsearch':
                    self.have_dirseach = 'have dirsearch' # co dirsearch
                    if x.getstatus() == False:
                        self.have_dirseach = 'dirsearch end' #  co dirsearch chay xong
                        result = x.getanswer()[DB_DIR]
                        self.run_nuclei(result)
                       
            if self.have_dirseach  == 'not run' :
                self.have_dirseach = 'dirsearch end'
                self.run_nuclei([self.url])
               
            if self.have_dirseach == 'have dirsearch':
                return True

            try:
                status = self.container.contariners_status()
                if status == False: return False
                return  "running" == status or "created" == status
            except Exception as e:
                return False
        except Exception as e:
            print(e)
            return False
    def getanswer(self):
        if self.getstatus(getanswer=True):
            return "Process running"
        
        self.answer = {}
        self.answer[DB_CVES] = []
        list_result = []
        try:
            with open(self.path_log  +  "nuclei.json") as file:
                datatxt = file.read().split('\n')
                
                file.close()
        except Exception as e:
            print(e)
        for data in datatxt:
            try:
                data_json_url = json.loads(data)
                self.answer[DB_CVES].append(data_json_url)
            except Exception as e:
                print(e)
        return self.answer
    def getoutput(self):
        try:
            if self.have_dirseach == "dirsearch end":
               return "running"
            elif self.have_dirseach == "have dirsearch":
                return "waitting"
            return "None"
        except Exception as e:
            print(e)
            return "None"
