#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database import put_recon
from target import get_target_id
from constvalue import *
from time import sleep
from queue import Queue
from threading import Thread
from datetime import datetime
from library import mergeDict
import importlib.util
import pathlib
from os import listdir
from os.path import isfile, join
def get_all_extension():
   
    path = str(pathlib.Path(__file__).parent.absolute()) +  "/tools/extension/"
    onlyfiles = [join(path, f) for f in listdir(path) if (isfile(join(path, f)) and f.endswith(".py"))]
    spec = [importlib.util.spec_from_file_location("module.name", paths) for paths in onlyfiles]
    foo = [importlib.util.module_from_spec(i) for i in spec]
    [spec[i].loader.exec_module(foo[i]) for i in range(len(foo))]
    return foo

def check_dirsearch():
    from tools.extension.dirsearch import  reconnaissance as reconnaissance_dirsearch
    dirsearch = reconnaissance_dirsearch()
    status  = dirsearch.run("http://fit.lqdtu.edu.vn")
    if (status == 0):
        print("running")
    else:
        print(status)
    while(dirsearch.getstatus()):
        print('running');
        print(dirsearch.getoutput())
        sleep(1)
    print("answer: ")
    print(dirsearch.getanswer())


def check_nmap():
    from tools.extension.nmap import  reconnaissance as reconnaissance_nmap
    dirsearch = reconnaissance_nmap()
    status  = dirsearch.run("https://mta.edu.vn")
    if (status == 0):
        print("running")
    else:
        print(status)
    while(dirsearch.getstatus()):
        print('running');
        sleep(1)
    print("answer: ")
    print(dirsearch.getanswer())  


def run(q, url, results):
    while not q.empty():
        work = q.get()                      #fetch new work from the Queue

        try:
            runprocess = work[1]
            status  = runprocess.run(url)            
            results[work[0]] = runprocess          #Store data back at correct index
        except:
            results[work[0]] = {}
        #signal to the queue that task has been processed
        q.task_done()
    return True

def thread_run(url, extension = ''):

    total_ans = {}
    total_ans["target_id"]  = get_target_id(url)[1]
    total_ans["date_start"] =  datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("start recon")
    func = []
    class_func = get_all_extension()
    for i in range(len(class_func)):
        cl = class_func[i].reconnaissance()
        if "*" + cl.info()['name'] + "*" in extension:
            func.append(class_func[i].reconnaissance())
    results = [{} for x in func];
    q = Queue(maxsize=0)
    for i in range(len(func)):
        q.put((i, func[i]))
    for i in range(10):
        worker = Thread(target=run, args=(q,url, results))
        worker.setDaemon(True) 
        worker.start()
    
    q.join()
    print(results)
    while(1):
        sleep(2)
        try:
            x = [i.getstatus() == False for i in results]
            print(x)
            print(results[0].getoutput())
            if all(x):
                break
        except:
            break
    total_ans['dir'] = []
    for i in results:
        res= i.getanswer()
        total_ans = mergeDict(total_ans,res)
    total_ans['dir'].append(url + '/')
    total_ans["date_end"] =  datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    put_recon(total_ans)

if __name__ == "__main__":
    thread_run("http://sinhvien.mta.edu.vn", '*wappalyzer**dirsearch*')
    #check_nmap()