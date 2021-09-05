#!/usr/bin/env python
# -*- coding: utf-8 -*-
import weakref
from configvalue import DICTIONLARY_HOME
from bson.objectid import ObjectId
from Database.database import connect, get_recon, put_recon, reconnaissance, update_recon
from Library.Target.target import Target, get_target_id
from configvalue import *
from time import sleep
from queue import Queue
from threading import Thread
from datetime import datetime
from Library.library import mergeDict
import importlib.util
import pathlib
from os import listdir, system
from os.path import isfile, join

#db 
class Reconnaissance: 
    _id = None
    recon_extensions = []
    recon_reports = []
    recon_result = {
        ""
    }

    target_id = None
    target_url = ''
    target_name = ''
    def get_all_extension(self):
       
        path = DICTIONLARY_HOME +  "Tools/ToolReconnai/extension/"
        onlyfiles = [join(path, f) for f in listdir(path) if (isfile(join(path, f)) and f.endswith(".py"))]
        spec = [importlib.util.spec_from_file_location("module.name", paths) for paths in onlyfiles]
        foo = [importlib.util.module_from_spec(i) for i in spec]
        [spec[i].loader.exec_module(foo[i]) for i in range(len(foo))]
        return foo

    def get_function_extension(self,  **kwargs):
        func = []
        class_func = self.get_all_extension()
        for i in range(len(class_func)):
            cl = class_func[i].reconnaissance()
            if 'reportPDF' == cl.info()['name']:
                if 'filereport' in kwargs:
                    func.append(class_func[i].reconnaissance("run", filereport=kwargs['filereport']))
            elif  cl.info()['name'] in self.recon_extensions:
                func.append(class_func[i].reconnaissance("run"))
        return func

    def run(self, q, results):
        while not q.empty():
            work = q.get()                      #fetch new work from the Queue
            try:
                runprocess = work[1]
                status  = runprocess.run(self.target_url)            
                results[work[0]] = runprocess     #Store data back at correct index
            except Exception as e:
                print("Error run tools", e)
                results[work[0]] = {}
            #signal to the queue that task has been processed
            q.task_done()
        return True

    def save_db(self):
        if self._id == None: 
            [status, result] = put_recon(self.recon_result)
            if status:
                self._id = result.inserted_id
            else: 
                print("Save to database fail", result)
        else:
            [status, result] = update_recon({"_id": ObjectId(self._id)}, self.recon_result)
        return  status

    def thread_run(self):

        self.recon_result = {}
        self.recon_result["target_id"]  = self.target_id
        self.recon_result["date_start"] =  datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print("start recon")
                
        if len(self.recon_reports) > 0:
            
            func=self.get_function_extension(filereport=self.recon_reports) 
            self.recon_result[DB_PDFRECON] = self.recon_reports

        else:
            func = self.get_function_extension()
        #add report 

        self.recon_result[DB_TOOLRECON] = []

        #end
        results = [{} for x in func];
        self.recon_reports
        q = Queue(maxsize=0)
        for i in range(len(func)):
            self.recon_result[DB_TOOLRECON].append(func[i].info()['name'])
            q.put((i, weakref.proxy(func[i])))
        for i in range(10):
            worker = Thread(target=self.run, args=(q,results,))
            worker.setDaemon(True) 
            worker.start()
        q.join()

        while(1):
            sleep(2)
            try:
                x = [i.getstatus(results) == False for i in results]
                temp = []
                print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), x)
                for i in results:
                    temp.append(i.getoutput())
                print(temp)
                if all(x):
                    break
            except Exception as e:
                print("Error start docker", e)
                break
        self.recon_result[DB_DIR] = [self.target_url]
        self.recon_result[DB_ENTRYPOINT] = []

        while len(func) > 0 :
            res= func[0].getanswer()
            try:
                import sys
                print(sys.getrefcount(func[0]))
                del func[0]
            except Exception as e:
                print("Error get answer tool", e)
            self.recon_result = mergeDict( self.recon_result,res)
        #total_ans['dir'].append(url + '/')
        self.recon_result["date_end"] =  datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.save_db()
    
    def update_extension(self, stringExtension):
        try:
            arrExten = stringExtension.split('*')
            self.recon_extensions = []
            for exten in arrExten:
                if exten != None and exten != "":
                    self.recon_extensions.append(exten)
        except Exception as e:
            raise e
        return True
    def update_report(self, arrReport):
        self.recon_reports = arrReport    
        
    
    def update_target(self, target_id):
        self.target_id = target_id
        target = Target(target_id)
        self.target_name = target.Name
        self.target_url = target.URL
    def update_reconid(self, recon_id):
        self._id = recon_id
        [status, data] = get_recon({"_id" : ObjectId(recon_id)})
        if status: 
            target = Target(data[0]['target_id'])
            self.target_name = target.Name
            self.target_url = target.URL
            self.target_id = target._id
            return True
        else:
            return False
#    def select_reconnaissance(self, reconid):



#end 



if __name__ == "__main__":
    connect()
    thread_run("http://ttnn.mta.edu.vn", '*screenshot**dirsearch*')
    #check_nmap()