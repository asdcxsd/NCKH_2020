import os 
import socket
import signal
import subprocess
class openport:
    process = []

    def __init__(self, portlocal,portpublic  ):
        self.openport(portlocal, portpublic)
    
    def __del__(self):
        try:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM) 
        except: 
            pass
    def forwarding(self, portlocal, portpublic):
        
        self.process = subprocess.Popen("sudo sshpass -p 'Asdq1w2e3!!' ssh -g -R 0.0.0.0:{}:0.0.0.0:{} lulu@40.74.72.51".format(portpublic, portlocal), shell = True, stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT)
    def netcat(self, hostname, port):
        netcat = 'xfce4-terminal --command "nc -nvlp {}"'.format(port)
        print ("Starting listener on {}".format(port))
        from subprocess import call
        call(netcat,shell=True)
    def listening(self, port):
        self.netcat("0.0.0.0",  port)
        return 0
    def openport(self, portlocal, portpublic):
        self.forwarding(portlocal, portpublic)
        self.listening(portlocal)
if __name__ == '__main__':
    openport(222, 2222)