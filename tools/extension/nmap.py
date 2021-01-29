#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import date
import re, shlex
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
import subprocess
class reconnaissance():
    ans = []
    path_log = ""
    process = None
    answer = []
    proc = ''
       

    def info(self):
        result = {}
        result['name'] = 'nmap'
        return result

    def run_nmap(self, inputurl, path_log, answer):
        try: 
            inputurl = inputurl.replace('https://', "").replace('http://', '').replace('/', '')
            tt = 'nmap -oN - "{}"'.format(inputurl)
            tt= shlex.split(tt)
            text = subprocess.check_output(tt)
            dataurl = str(text)
            x = re.findall("n[0-9]+\/", dataurl)
            x = [i[1:-1]for i in x]
            #dataurl = dataurl.split('\n')[:-1]
            self.answer = {}
            self.answer[DB_PORT] = x

        except Exception as e:
            print("Error run process:", e)
    def run(self, inputurl):
        if self.getstatus() == True:
            print("Process busy")
            return "Process busy"
        self.process = Thread(target=self.run_nmap, args = (inputurl, self.path_log , self.answer))
        self.process.start()

    def getstatus(self):
        try:
            return self.process.is_alive()
        except Exception as e:
            print(e)
            return False
    def getanswer(self):
        if self.getstatus():
            return "Process running"
        return self.answer
    def getoutput(self):
        return "running"
    
