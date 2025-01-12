from Framework.Library.Function.Function.PocSuite.Function import encode_data_input_poc
from Framework.Library.Function.Function.PocSuite.lib.core.register import load_file_to_module
import os
from Framework.Library.Function.Function.PocSuite.api import get_results, init_pocsuite
from Framework.Library.Function.Function.PocSuite.api import paths as PATHS, get_results ,start_pocsuite, init_pocsuite, POC_SCAN, load_file_to_module

def createScan(url, pocs ,mode = 'verify', data = ""):
    config = {
    'url': url,
    'poc': pocs,
    'mode': mode,
    'referer' : encode_data_input_poc(data)
    }
    init_pocsuite(config)

def check_result(url, poc,  mode):
    ans = []
    dataget = get_results().copy()
    for res in dataget:
        if (res['target'] == url and res['mode'] == mode and res['app_name'] == poc): # check value 
            if(res['status'] == 'success'):
                temp = {
                    "result": res['result'],
                    "app_name" : res["app_name"],
                    "created" : res['created']
                }
            
                ans.append([True, temp])
            else:
                ans.append([False, poc])
            get_results().remove(res)
    return ans
def get_all_class_tool():
    try:
        exists_poc_with_ext = list(
            filter(lambda x: x not in ['__init__.py', '__init__.pyc'], os.listdir(PATHS.POCSUITE_POCS_PATH)))
        exists_pocs = [os.path.splitext(x)[0] for x in exists_poc_with_ext]
        return exists_pocs
    except Exception as e:
            return str(e)
def get_infomation_of_tool(name_poc):
    if not name_poc.endswith('.py'):
        name_poc += '.py'
    init_pocsuite({})
    try:
        poc_filename = os.path.join(PATHS.POCSUITE_POCS_PATH, name_poc )
        mod = load_file_to_module(poc_filename)
        return mod.get_infos()
    except Exception as e:
        return {
            "error": str(e)
        }