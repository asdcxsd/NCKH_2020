from hashlib import new
from logging import disable
import os
from time import sleep
from POCURI import POCURI
from urllib.parse import urlparse
import subprocess
from queue import Queue
from reconnaissance import thread_run as reconnaissance
from database import get_recon, connect, put_exploit_cve, get_exploit_cve
from target import get_target_url
from library import mergeDict
from threading import Thread
from datetime import datetime
from tools_run.openport import openport
class run_scan():
    target = ""
    target_id = ""
    info_target = []
    ans = []
    def __init__(self, target = "", target_id = "", recon = False):
        self.target = get_target_url(target_id)
        self.target_id = target_id
        if recon: 
            reconnaissance(self.target)
        
    def get_infos(self):

        data_find = {
            "target_id": self.target_id
        }
        print(self.target)
        status, data = get_recon(data_find)
        ans = datetime(2000,1,1)

        for info in data:
            date = info['date_end']
            date = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
            if (date > ans):
                ans = date
                self.info_target = info 
       
    def get_dir(self):
        self.get_infos()
        return self.info_target['dir']
    def runpoc_with_url(self, entrypoint, info, disable_poc = []):
         
        try:
            newpoc = POCURI();
            newpoc.find_language(info)
            newpoc.update_disable_poc(disable_poc)
            status, ans  = newpoc.run(entrypoint)            
            
        except Exception as e:
            ans = str(e)
        #signal to the queue that task has been processed
        
        return ans
    def run_poc(self,entrypoint, pocs):
        newpoc = POCURI(entrypoint);
        newpoc.run_shell([pocs]) # run entrypoint with pocs
    def run(self):
        try:
            self.get_infos() #get info from db
            dir_scan = self.get_dir() # get dir from info
            results = []; #last result 
            disable_pocs = [] # poc not run
            for i in dir_scan:
                ans = self.runpoc_with_url(i ,self.info_target['framework'], disable_pocs) # running
                for poc in ans: #ans
                    if (poc['status'] == 'success'):
                        save_poc = {}
                        save_poc['result'] = poc['result']
                        save_poc['target_id'] = self.target_id
                        save_poc['app_name'] = poc['app_name']
                        save_poc['target'] = self.info_target['target']
                        save_poc['date_check'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        results.append(save_poc)
                        disable_pocs.append(poc['app_name']) # don't scan with this poc
            for res in results:
                if put_exploit_cve(res):
                    print("Save poc:", res)
            return "success"
        except Exception as e:
            return str(e)