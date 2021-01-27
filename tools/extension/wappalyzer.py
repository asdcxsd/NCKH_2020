#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, shlex
from urllib.parse import urlsplit
import json
import os
from threading import Thread
from constvalue import *
from subprocess import Popen, PIPE, STDOUT
import subprocess
class reconnaissance_wappalyzer():
    ans = []
    path_log = ""
    process = None
    answer = []
    proc = ''
       


    def run_wappalyzer(self, inputurl, path_log, answer):
        try: 
            tt = 'python3 ./tools/find_domain_and_technology/start.py {}'.format(inputurl)
            tt= shlex.split(tt)
            text = subprocess.check_output(tt)
            text=text.decode('ascii').strip('\n').replace('\'', '"')
            #dataurl = dataurl.split('\n')[:-1]
            self.answer = {}
            self.answer[DB_TECHNOLOGY] = json.loads(text)

        except Exception as e:
            print("Error run process:", e)
    def run(self, inputurl):
        if self.getstatus() == True:
            print("Process busy")
            return "Process busy"
        self.process = Thread(target=self.run_wappalyzer, args = (inputurl, self.path_log , self.answer))
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
    