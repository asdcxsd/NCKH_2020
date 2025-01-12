#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Library.manager_docker import ContainersDocker
import os
from datetime import date
import re
from sys import path
from urllib.parse import urlsplit
import hashlib
import os, datetime, binascii
import pathlib, base64
import shutil, json
import random, string
from threading import Thread
from configvalue import *
from subprocess import Popen, PIPE, STDOUT
class reconnaissance():
    ans = []
    url = ''
    name  = "dirsearch:v0.4.1"
    filename = 'dirsearch.py'
    path_log = ""
    container = None
    have_nmap = "finding"
    process = []
    answer = []

    def __init__(self, *args, **kwargs ):
        if "run" in args: 
            print("dirsearch")
            self.name  = "dirsearch:v0.4.1"
        self.path_log != ""
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

    def run_dirsearch(self, inputurl, answer):
        
        try:
            self.container = ContainersDocker(self.name)
            self.url = inputurl
            self.make_path_log();
            volumes = {self.path_log: {"bind": "/tmp/" , "mode":"rw"}}
            command = "-u " + inputurl + "  --json-report=/tmp/dirsearch.json"
            self.container.run_containers_cmd(volumes=volumes, command=command, detach=True  )
        except Exception as e:
            print("Error run process:", e)
    def run(self, inputurl):
        if self.getstatus() == True:
            print("Process busy")
            return "Process busy"
        self.run_dirsearch(inputurl , self.answer)

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
        
        self.answer = {}
            
        self.answer[DB_DIR] = []
        self.answer[DB_ENTRYPOINT] = []
        list_result = []
        try:
            with open(self.path_log  +  "dirsearch.json") as file:
                data_json_url = json.loads(file.read())
                file.close()
        except Exception as e:
            print(e)
            self.answer[DB_DIR].append(self.url)
            return self.answer
        if self.url not in self.answer[DB_DIR] : 
            self.answer[DB_DIR].append(self.url)
        for key, val in data_json_url.items():
            if key == "time":
                continue
            self.answer[DB_DIR].append(key)
            key_path = key[:-1]
            for path in val:
                try:
                    if (path['status'] >= 300 and path['status']  < 400) :
                        self.answer[DB_DIR].append(key_path + path['path'] + "/")
                    if path['status'] == 403 and path['path'][-1] == '/':
                        self.answer[DB_DIR].append(key_path + path['path'])
                    if path['status'] <300: 
                        self.answer[DB_ENTRYPOINT].append(key_path + path['path'])
                    if  path['status'] >= 500 and  path['content-length'] > 0:
                        self.answer[DB_ENTRYPOINT].append(key_path + path['path'])
                    
                        
                except Exception as e: 
                    print("Error with path: ", e)
        
        return self.answer

    def getoutput(self):
        return "running"
        
    

if __name__ == "__main__": 
    dirsearch  = reconnaissance()   
    dirsearch.run_dirsearch("http://192.168.133.177")
