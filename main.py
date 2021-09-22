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
from library import mergeDict
from threading import Thread
from datetime import datetime
from tools_run.openport import openport
class run_scan():
    target = ""
    info_target = []
    ans = []
    def __init__(self, tar, recon = False):
        parsed_uri =  urlparse(tar)
        self.target = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        if recon: 
            reconnaissance(self.target)
        
    def get_infos(self):

        data_find = {
            "target": self.target
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
    def runpoc_with_url(self, url, info, disable_poc = []):
         
        try:
            newpoc = POCURI();
            newpoc.find_language(info)
            newpoc.update_disable_poc(disable_poc)
            status, ans  = newpoc.run(url)            
            
        except Exception as e:
            ans = str(e)
        #signal to the queue that task has been processed
        
        return ans
    def run_poc(self,url, pocs):
        newpoc = POCURI(url);
        newpoc.run_shell([pocs])
    def run(self):
       
        self.get_infos()
        dir_scan = self.get_dir()
        results = [];
        disable_pocs = []
        for i in dir_scan:
            ans = self.runpoc_with_url(i ,self.info_target['framework'], disable_pocs)
            for poc in ans:
                if (poc['status'] == 'success'):
                    save_poc = {}
                    save_poc['result'] = poc['result']
                    save_poc['target_id'] = poc['url']
                    save_poc['app_name'] = poc['app_name']
                    save_poc['target'] = self.info_target['target']
                    save_poc['date_check'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    results.append(save_poc)
                    disable_pocs.append(poc['app_name'])

        for res in results:
            if put_exploit_cve(res):
                print("Save poc:", res)

    

if __name__ == "__main__":
    
    #a = POCURI()
    #print(a.run('http://ttnn.mta.edu.vn/'))
    target = 'http://ttnn.mta.edu.vn'
    connect()
    #reconnaissance(target)

    pocr = run_scan(target, recon= False)
    #pocr.run()
    [status, data] = get_exploit_cve({"target": target})
    data = data[0]
    url = data['url']
    openport(2222)
    
    pocr.run_poc(url, data)
    

