from logging import disable
from Framework.Library.Function.Function.PocSuite.lib.controller.controller import runtime_check
import unittest, os
from urllib.parse import urlparse

from Framework.Library.Function.Function.PocSuite.api import paths as PATHS, get_results ,start_pocsuite, init_pocsuite, POC_SCAN, paths, load_file_to_module
#doi appname la ten file 
class POCURI():
    url = "";
    type = "";
    language  = [];
    disable_poc = [];
    def __init__(self, url = ''):
        self.url = url
        self.find_language()
    def update_disable_poc(self, pocs):
        self.disable_poc = pocs
    def check_disable_poc(self, pocs):
        ans = []
        for i in pocs:
            if (i not in self.disable_poc): ans.append(i)
        return ans
    def setUp(self, pocs ,mode = 'verify', data = ""):
        self.config = {
            'url': self.url,
            'poc': pocs,
            'mode': mode,
            'referer' : data
        }
        init_pocsuite(self.config)

    def get_all_pocs(self): # get all poc in db
        try:
            exists_poc_with_ext = list(
                filter(lambda x: x not in ['__init__.py', '__init__.pyc'], os.listdir(PATHS.POCSUITE_POCS_PATH)))
            exists_pocs = [os.path.splitext(x)[0] for x in exists_poc_with_ext]
            return exists_pocs
        except Exception as e:
            return str(e)
    
    def run_check_poc(self, listcheck_pocs):
        if (len(listcheck_pocs) == 0):
            return [];
        ans = []
        self.setUp(listcheck_pocs);
        start_pocsuite()
        ans = self.verify_result('verify')
        return ans

    def run_poc(self, listpocs):
        if (len(listpocs) == 0):
            return []
        pocs = [x['app_name'] for x in listpocs]
        self.setUp(pocs, 'attack')
        start_pocsuite()
        ans = self.verify_result('attack')
        #print(ans)
        return ans

    def run_shell(self, listpocs, datainput):
        if (len(listpocs) == 0):
            return []
        pocs = [x['app_name'] for x in listpocs]
        datainput.update(listpocs[0])
        input = {
            "input": datainput
        }
        self.setUp(pocs, 'shell', input)
        start_pocsuite()
        ans = self.verify_result('shell')
        #print(ans)
        return ans

    def get_info_poc(self, name_poc):
        try:
            init_pocsuite({})
            poc_filename = os.path.join(paths.POCSUITE_POCS_PATH, name_poc )
            mod = load_file_to_module(poc_filename)
            return mod.get_infos()
        except Exception as e:
            print("Error load info poc", e)
            return 0
        
    def filter_poc_with_language(self, language, pocs, dir, enablepocs):
        ans = []
        for poc in pocs:
            res = self.get_info_poc(poc + '.py')
            if res == 0 : continue
            if "*" + poc + "*" in enablepocs:
                ans.append(poc)
            else:
                try:
                    if (res['appPowerLink']['typescan'] == POC_SCAN.EXPLOITS.SERVER and dir):
                        continue
                except Exception as e:
                    print("Don't have typescan: ", e)
                
            
                for lang in language:
                    if lang in res['appPowerLink']['language']: 
                        ans.append(poc)
                        break
        return ans
    
    def check_url_have_dir(self, url):
        parsed_uri = urlparse(url)
        result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return not (parsed_uri.path == '/' or parsed_uri.path == '')
    
    def find_language(self, framework = {}):
        self.language = []
        if (framework == {}):
            self.language = [POC_SCAN.LANGUAGE.ASP, POC_SCAN.LANGUAGE.JS, POC_SCAN.LANGUAGE.PYTHON , POC_SCAN.LANGUAGE.PHP, POC_SCAN.LANGUAGE.JAVA ]
        try:
            for x in framework['Web frameworks']:
                if ("asp" in x.lower()): 
                    self.language.append(POC_SCAN.LANGUAGE.ASP)
        except:
            self.language = [POC_SCAN.LANGUAGE.ASP, POC_SCAN.LANGUAGE.JS, POC_SCAN.LANGUAGE.PYTHON , POC_SCAN.LANGUAGE.PHP, POC_SCAN.LANGUAGE.JAVA ]

    def run(self, url, pocs_enable):
        self.url  = url;
        
        option_pocs = self.get_all_pocs();
        option_pocs = self.filter_poc_with_language(self.language, option_pocs, self.check_url_have_dir(self.url), pocs_enable)
        option_pocs = self.check_disable_poc(option_pocs);
        listcheck_pocs = self.run_check_poc(option_pocs)
        
        ans = self.run_poc(listcheck_pocs)
        return (ans != []), ans
   