#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import date
import re
from sys import flags, path
from urllib.parse import urlsplit
import hashlib
import os, datetime, binascii
import pathlib, base64
import shutil
import random, string
from threading import Thread
from constvalue import *
from subprocess import Popen, PIPE, STDOUT
from constvalue import *
import docker
import requests
class reconnaissance():
    ans = []
    path_log = ""
    process = None
    answer = []
    proc = ''
    url = ''
    have_dirseach = 0
    classcalling = 0
    def __init__(self):
        print("screenshot")
        
        try:
            client = docker.from_env()
            client.api.start('web-screenshot')
        except Exception as e:
            print(e)
        reconnaissance.classcalling += 1
        print("sreenshot start ", reconnaissance.classcalling )
    def __del__(self):
        reconnaissance.classcalling -= 1
        print("sreenshot stop ", reconnaissance.classcalling )
        if reconnaissance.classcalling <= 0: 
            try:
                client = docker.from_env()
                client.api.stop('web-screenshot')
            except Exception as e:
                print(e)
    def info(self):
        result = {}
        result['name'] = 'screenshot'
        result['service'] = 'webservice port 2341'
        return result

    def make_path_log(self):
        if self.path_log != '':
            return 
        self.path_log = os.path.dirname(os.path.realpath(__file__)) + '/../../public/'
        self.path_log +=  ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) +  str(datetime.datetime.now().timestamp()).split('.')[0] +'/'
        if not os.path.exists(self.path_log):
            os.mkdir(self.path_log)
   
    def delete_path_log(self):
        try:
            shutil.rmtree(self.path_log)
        except Exception as e:
            print(str(e))

    def run_screenshot(self, result):
        self.make_path_log();
        answer = []
        try:
            for entrypoint in result:
                try:
                    req = requests.get("http://localhost:2341/?url=" + entrypoint)
                    filename = self.path_log + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) +  str(datetime.datetime.now().timestamp()).split('.')[0] + ".png"
                    with open(filename, "wb") as file:
                        file.write(req.content)
                        file.close() 
                    temp = {
                        "entrypoint" : entrypoint,
                        "image" : filename.split('../')[-1]
                    }
                except Exception as e:
                    temp = {
                        "entrypoint" : entrypoint,
                        "error" : str(e)
                    }
                answer.append(temp)
            self.answer  =  {
                DB_SCREENSHOT : answer
            }
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
                if self.have_dirseach != 2 and x.info()['name'] == 'dirsearch':
                    self.have_dirseach = 1
                    if x.getstatus() == False:
                        self.have_dirseach = 2
                        result = x.getanswer()[DB_ENTRYPOINT]
                        self.process = Thread(target=self.run_screenshot, args = (result, ))
                        self.process.start()
            if self.have_dirseach  == 0 :
                self.have_dirseach = 2
                self.process = Thread(target=self.run_screenshot, args = ([self.url],))
                self.process.start()
            if self.have_dirseach == 1:
                return True

            return self.process.is_alive()
        except Exception as e:
            print(e)
            return False
    def getanswer(self):
        if self.getstatus(getanswer=True):
            return "Process running"

        return self.answer
    def getoutput(self):
        try:
            if self.have_dirseach == 2:
               return "running"
            elif self.have_dirseach == 1:
                return "waitting"
            return "None"
        except Exception as e:
            print(e)
            return "None"
    
    def exitprocess(self):
        if self.proc != '': 
            try:
                self.proc.kill()
            except Exception as e:
                print(e)
        try:
            self.getanswer()
        except Exception as e:
            print(e)