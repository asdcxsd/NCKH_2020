#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Library.manager_docker import ContainersDocker
import os
from datetime import date
import re, shlex
from sys import path
from urllib.parse import urlparse, urlsplit
import hashlib
import os, datetime, binascii
import pathlib, base64
import shutil
import random, string
import xmltodict
from threading import Thread
from configvalue import *
from subprocess import Popen, PIPE, STDOUT
import subprocess
class reconnaissance():
    ans = []
    path_log = ""
    name  = "uzyexe/nmap"
    filename = 'nmap.py'
    process = None
    answer = []
    proc = ''
    def __init__(self, *args, **kwargs):
        if "run" in args:
            print("nmap")       
            self.name  = "uzyexe/nmap"
    def info(self):
        result = {}
        result['name'] = 'nmap'
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

    def run_nmap(self, inputurl, path_log, answer):
       
        try:
            self.container = ContainersDocker(self.name)
            self.url = inputurl
            self.make_path_log();
            volumes = {self.path_log: {"bind": "/tmp/" , "mode":"rw"}}
            command = " -Pn " + inputurl + " --open -oX  /tmp/nmap.xml"
            self.container.run_containers_cmd(volumes=volumes, command=command, detach=True  )

        except Exception as e:
            print("Error run process:", e)
    def run(self, inputurl):
        if self.getstatus() == True:
            print("Process busy")
            return "Process busy"
        parsed_uri =  urlparse(inputurl)
        inputurl = '{uri.netloc}'.format(uri=parsed_uri)
        inputurl = inputurl.split(":")[0]
        self.run_nmap(inputurl, self.path_log , self.answer)
       

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
        self.answer[DB_PORT] = []
        with open(self.path_log  +  "nmap.xml") as file:
            data_json_url =xmltodict. parse(file. read())
            file.close()
        try:
            ports = data_json_url['nmaprun']['host']['ports']['port']
            for port in ports: 
                save_port = {
                    "port" : port['@portid']
                }
                try:
                    save_port['service'] = port['service']['@name']
                except:
                    pass
                self.answer[DB_PORT].append(save_port)

        except Exception as e:
            print(e)

        return self.answer

    def getoutput(self):
        return "running"
    
