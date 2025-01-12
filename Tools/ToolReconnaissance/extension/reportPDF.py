from Framework.Library.Function.Function.PocSuite.lib.controller.controller import start
import random
from configvalue import DB_DIR, DB_ENTRYPOINT, DB_VULN, DICTIONLARY_HOME
from Tools.ToolReconnai.report.acunetix import quick_report as report_acunetix
from threading import Thread

def get_report_acunetix(filename):
    gen = report_acunetix(filename)
    data =gen.getdata()
    temp = {}
    for ele in data[0]:
        try:
            temp[ele[0]] = ele[1]
        except Exception as e:
            print("Error report infomation acunetix", e)
    result = {
        'target': temp
    }
    verify=  []
    for i in range(2, len(data)):
        str2 = ''.join(data[i][0])
        if (str2.find("(verified)") >= 0):
            data[i][0] = str2[:str2.find('(verified)')]
            verify.append(True)
        else:
            verify.append(False)
    result['data'] = []
    for index, i in enumerate(data[2:], start=0):
        try:
            datatemp = {
            "Vuln" : "".join(i[0]),
            "Item" :  i[1][1], 
            "Verify" : verify[index],
            "Parameter" : i[2][1],
            "Request" :   "".join(i[4])
            } 
            result['data'].append(datatemp)
        except Exception as e:
            print("Error report exception fomat detail vuln", e)
    
    return result



class reconnaissance():
    ans = []
    url = ''
    filereport = []
    answer = {}

    def __init__(self, *args, **kwargs ):
        print("report PDF acunetix")
        if 'filereport' in kwargs:
            self.filereport = kwargs['filereport']
        else: 
            print("Not file report")
        
    def info(self):
        result = {}
        result['name'] = 'reportPDF'
        result['type'] = "internal"
        return result

    def __del__(self):
        try:
            
            print("Success Report")
                
        except Exception as e:
            print(e)

    def run_reportPDF(self, inputurl):
        
        try:
            path = DICTIONLARY_HOME  + "PUBLIC/REPORTS/"
            for report in self.filereport:
                data = get_report_acunetix(path + report)
            self.answer[DB_VULN] = data['data']
        except Exception as e:
            print("Error run process:", e)
    def run(self, inputurl):
        if self.getstatus() == True:
            print("Process busy")
            return "Process busy"
        process = Thread(target=self.run_reportPDF, args = (inputurl,))
        process.start()
        self.process= process
        return 0
    def getstatus(self, result= ''):
        try:
            return self.process.is_alive()
        except Exception as e:
            print(e)
            return False
    def getanswer(self):
        if self.getstatus():
            return "Process running"
    
        
        return self.answer

    def getoutput(self):
        return "running"
        
    

if __name__ == "__main__": 
    dirsearch  = reconnaissance()   
    dirsearch.run_dirsearch("http://192.168.133.177")