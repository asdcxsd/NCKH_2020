
from Library.Exploit.function_pocs import copy_pocs, delete_poc, unzip_file
from configvalue import FOLDER_POCS, UPDATE_FOLDER_POCS
import json
import os
import shutil, zipfile
from Library.Exploit.POCURI import POCURI


def function_get_infomation():
    POC = POCURI();
    pocs = POC.get_all_pocs()
    ans = []
    for poc in pocs:
        res = POC.get_info_poc(poc + '.py')
        info = {
            "ID" : res['appVersion'],
            "Name" : res['name'],
            "Date" : res['vulDate'],
            "pocName" : res['appName'] 

        }
        ans.append(info)
    return ans

def function_get_infomation_of_poc(namepoc):
    POC = POCURI();
    res = POC.get_info_poc(namepoc + '.py')
    return res

def function_import_poc(namefile):
    try:
        namefile = namefile[:-4]
        path = UPDATE_FOLDER_POCS + namefile 
        zipfile = unzip_file(path + ".zip", UPDATE_FOLDER_POCS)
        folder = zipfile.unzipfolder()
        status = copy_pocs(path + "/", FOLDER_POCS)
    except Exception as e:
        raise e
    finally: 
        del zipfile
    return status
def function_delete_poc(namepoc):
    infopoc = function_get_infomation_of_poc(namepoc)
    return delete_poc(infopoc)