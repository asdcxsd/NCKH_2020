#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import random
import string
from Framework.Library.Output.OutputReport.Init.Gen_Case import gen_report_case_from_json
from copy import Error
from random import randint
from Framework.Valueconfig import ValueStatus
from configvalue import PUBLIC_FOLDER
import os
from datetime import date
import re
from sys import path
from urllib.parse import urlsplit
import hashlib
import os, time, binascii, json

from subprocess import Popen, PIPE, STDOUT

from Framework.Library.Module import Module
from Framework.Library.Output.OutputReport.output import ModuleOutput
from Framework.Library.Output.OutputReport.input import ModuleInput
from Framework.Library.Function.openport import OpenPort
from Framework.Library.Function.Function.POC import POC

class ModuleFramework(Module):
    name = "OutputReport"
    type_module = "Module_Output"
    path_input_class = "/input.py"
    path_output_class = "/output.py"
    ans = []
    url = ''
    filename = 'output_report.py'
    path_log = ""
    input_module = None
    config_module = None
    status = ''
    result_of_other_tool = {}


    def __init__(self):
        self.status = ValueStatus.Creating
    def info(self):
        result = {}
        result['name'] = self.name
        result['typemodule'] = self.type_module
        result['type'] = "offline"
        result['version'] = "1.0"
        return result
    def stop(self):
        self.status = ValueStatus.Stopping
       
    def start(self):
        # run 
        self.output_module = ModuleOutput()
        self.path_save =  ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) +  str(datetime.datetime.now().timestamp()).split('.')[0] + ".pdf"
        self.status = ValueStatus.Running

        try:
            gen_report_case_from_json(self.input_module.data, PUBLIC_FOLDER + self.path_save)
            self.status = ValueStatus.Success
            self.output_module.OUTPUT_REPORT_PDF.append(self.path_save)
        except Exception as e:
            print("Exception: ", self.name, e)
            self.status = ValueStatus.Error

      
    def get_status(self):
        return self.status
    def set_input_module(self, input):
        
        try:
            self.input_module = ModuleInput()
            for key, list_data in input.items():
                if key == 'db_process':
                    list_data = {
                        "OTHER_PROCESS" : [list_data]
                    }
                if not isinstance(list_data, list):
                    list_data = [list_data]
                for data in list_data:
                    temp_module = ModuleInput()
                    temp_module.try_parse(data)
                    self.input_module.extend(temp_module)
        except Exception as e:
            print("Error get input for Report", e)
    def get_output_module(self):
        return self.output_module




if __name__ == "__main__": 
      
    pass