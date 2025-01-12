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
    name  = "wappalyzer/cli"
    filename = 'wappalyzer.py'
    path_log = ""
    container = None
    have_nmap = "finding"
    process = []
    answer = []

    def __init__(self, *args, **kwargs ):
        if "run" in args: 
            print("wappalyzer")
            self.name  = "wappalyzer/cli"
        self.path_log != ""
    def info(self):
        result = {}
        result['name'] = 'wappalyzer'
        result['type'] = "offline"
        return result

    def __del__(self):
        try:
            if self.container != None: 
                if self.container.remove_containers():
                    print("Remove Container OK")
            print("Remove Container OK")    
        except Exception as e:
            print(e)

    def run_wappalyzer(self, inputurl, answer):
        
        try:
            self.container = ContainersDocker(self.name)
            self.url = inputurl
            command = inputurl
            self.container.run_containers_cmd( command=command, detach=True  )

        except Exception as e:
            print("Error run process:", e)
    def run(self, inputurl):
        if self.getstatus() == True:
            print("Process busy")
            return "Process busy"
        self.run_wappalyzer(inputurl , self.answer)

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
        status, anstext  = self.container.get_comtainers_output()
        
        self.answer = {}
        if status == False: 
            self.answer[DB_TECHNOLOGY]= {}
        else: 
            datajson  = json.loads(anstext)
            
            result = {}
            for technolo in datajson['technologies']:
                for i in technolo['categories']:
                    try:
                        value = technolo['name'] + "|" + (technolo['version'] if technolo['version'] != None else "")
                        valuekey = i['name']
                        if valuekey in result.keys():    
                            result[valuekey].append(value)
                        else:
                            result[valuekey] = [value]
                    except Exception as e:
                        print(e)
            self.answer[DB_TECHNOLOGY] =result
        return self.answer

    def getoutput(self):
        return "running"
        
    

if __name__ == "__main__": 
    dirsearch  = reconnaissance()   
    dirsearch.run_dirsearch("http://192.168.133.177")
