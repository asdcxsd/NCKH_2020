import random
from configvalue import DB_DIR, DB_ENTRYPOINT, DB_VULN, DICTIONLARY_HOME
from Tools.ToolReconnai.report.acunetix import quick_report as report_acunetix
from threading import Thread

def get_report_acunetix(filename):
    gen = report_acunetix(filename)
    data =gen.getdata()
    result = {
        'target': data[0]
    }
    data = [{
        "Vuln" : i[0],
        "Item" :  i[1][1], 
        "Verify" : random.choice([True, False, False, False]),
        "Parameter" : i[2][1],
        "Request" :  i[4]
    } for i in data[2:]]
    result['data'] = data
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