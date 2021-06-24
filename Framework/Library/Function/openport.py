import threading
from Framework.Library.Module import Status
from Framework.Valueconfig import ValueStatus
import os 
import socket
import signal
import subprocess, time
import requests
class OpenPort:
    port = 1
    URL_server = "http://13.76.188.147:5000"
    status = ValueStatus.Creating
    def __init__(self, URL_server):
        self.URL_server = URL_server
    
    def openport(self,portpublic):
        Params = {
            'port': portpublic
        }
        self.port = portpublic
        self.status = ValueStatus.Running
        req = requests.get(self.URL_server + "/openport", params=Params)
        if (req.status_code == 200):
            self.run_check()
            return True
        return False
    def run_check(self):
        process = threading.Thread(target=self.check_connect_thread, args=())
        process.start()
    
    def check_connect_thread(self, timeout = 10):
        Params = {
            'port' :  self.port
        }
        try:
            req = requests.get(self.URL_server + "/check_connect", params=Params)
            if  (req.status_code == 200):
                self.status = ValueStatus.Success

        except Exception as e:
            print("Error check connect port", e)
            self.status = ValueStatus.Error
    def check_connect(self):
        return self.status

    def send(self, data):
        Params = {
            'port' :  self.port,
            'message' : data
        }
        req = requests.get(self.URL_server + "/send", params=Params)
        return (req.status_code == 200)

    def receive(self, length=4096):
        Params = {
            'port' :  self.port,
            'length' : length
        }
        req = requests.get(self.URL_server + "/receive", params=Params)
        return (req.status_code == 200)
if __name__ == '__main__':
    OpenPort(2222)