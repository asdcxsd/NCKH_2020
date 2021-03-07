import os 
import socket
import signal
import subprocess, time
import requests
class openport:
    port = 1
    URL_server = "http://13.76.188.147:5000"
    def __init__(self, publicip, portpublic  ):
        self.URL_server = "http://" + publicip + ":5001"
        self.port = portpublic
        self.openport(portpublic)
    
    def openport(self,portpublic):
        Params = {
            'port': portpublic
        }
        req = requests.get(self.URL_server + "/openport", params=Params)
        return (req.status_code == 200)
    
    def check_connect(self, timeout = 10):
        Params = {
            'port' :  self.port,
            'timeout' : timeout
        }
        req = requests.get(self.URL_server + "/check_connect", params=Params)
        if  (req.status_code == 200):
            return req.text
        else : return None
        
    def send(self, data):
        Params = {
            'port' :  self.port,
            'message' : data
        }
        req = requests.get(self.URL_server + "/send", params=Params)
        return (req.status_code == 200)

    def recevie(self, length=4096):
        Params = {
            'port' :  self.port,
            'length' : length
        }
        req = requests.get(self.URL_server + "/recevie", params=Params)
        return (req.status_code == 200)
if __name__ == '__main__':
    openport(2222)