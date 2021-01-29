#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import date
import re
from sys import path
from urllib.parse import urlsplit
import hashlib
import os, datetime, binascii
import pathlib, base64
import shutil
import random, string
from threading import Thread
from constvalue import *
from subprocess import Popen, PIPE, STDOUT
class reconnaissance():
    ans = []
    path_log = ""
    process = None
    answer = []
    proc = ''
    def __init__(self):
        self.make_path_log();

    def info(self):
        result = {}
        result['name'] = 'dirsearch'
        return result

    def __del__(self):
        try:
            self.exitprocess();
            self.delete_path_log();
        except Exception as e:
            print(e)
    def make_path_log(self):
        if self.path_log != "":
            return 
        self.path_log = os.path.dirname(os.path.realpath(__file__)) + '/../log/'
        url = ""
        self.path_log +=  ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) +  str(datetime.datetime.now().timestamp()).split('.')[0] +'/'
        if not os.path.exists(self.path_log):
            os.mkdir(self.path_log)
   
    def delete_path_log(self):
        try:
            shutil.rmtree(self.path_log)
        except Exception as e:
            print(str(e))

    def run_dirsearch(self, inputurl, path_log, answer):
        try: 
            tt = 'python3 ./tools/dirsearch/dirsearch.py -u {} -e . --simple-report="{}"'.format(inputurl, path_log +"dirsearch.txt")
            self.proc = Popen(tt, stdout = PIPE,  stderr = STDOUT, shell = True)
        
        except Exception as e:
            print("Error run process:", e)
    def run(self, inputurl):
        if self.getstatus() == True:
            print("Process busy")
            return "Process busy"
        self.run_dirsearch(inputurl, self.path_log , self.answer)

        return 0
    def getstatus(self):
        try:
            return self.proc.poll() is None
        except Exception as e:
            print(e)
            return False
    def getanswer(self):
        if self.getstatus():
            return "Process running"
        
        with open(self.path_log  +  "dirsearch.txt") as file:
            dataurl = str(file.read())
            dataurl = dataurl.split('\n')[:-1]
            self.answer = {}
            self.answer[DB_DIR] = []
            self.answer[DB_ENTRYPOINT] = []
            for i in dataurl:
                try:
                    if i[-1] =='/':
                        if (i not in self.answer[DB_DIR]): 
                            self.answer[DB_DIR].append(i)
                    else:
                        if (i not in self.answer[DB_ENTRYPOINT]): 
                            self.answer[DB_ENTRYPOINT].append(i)
                except Exception as e: 
                    print("Error with path: ", i, e)
        return self.answer
    def getoutput(self):
        try:
            out = str(self.proc.stdout.readline())
            if ('Task Completed' in out):
                self.exitprocess();
            x = re.findall("[0-9]+\.[0-9]+%", out)
            if (x == []): return "unknow"

            return x[-1]
            
        except Exception as e:
            print(e)
            return "None"
    
    def exitprocess(self):
        if self.proc != '': 
            try:
                self.proc.stdout.close()
                self.proc.kill()
            except Exception as e:
                print(e)
        try:
            self.getanswer()
        except Exception as e:
            print(e)