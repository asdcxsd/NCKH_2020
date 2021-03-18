from configvalue import DB_DIR, DB_ENTRYPOINT, DB_VULN
from Tools.ToolReconnai.report.acunetix import quick_report as report_acunetix


def get_report_acunetix(filename):
    gen = report_acunetix(filename)
    data =gen.getdata()
    data = [{
        "Vuln" : i[0],
        "Item" :  i[1][1], 
        "Parameter" : i[2][1],
        "Request" :  i[4]
    } for i in data[2:]]
    return data



class reconnaissance():
    ans = []
    url = ''
    filereport = []
    answer = []

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

    def run_reportPDF(self, inputurl, answer):
        
        try:
            print("run")
        except Exception as e:
            print("Error run process:", e)
    def run(self, inputurl):
        if self.getstatus() == True:
            print("Process busy")
            return "Process busy"
        self.run_reportPDF(inputurl , self.answer)

        return 0
    def getstatus(self, result= ''):
        try:
            
            if status == False: return False
            return  "running" == status or "created" == status
        except Exception as e:
            return False
    def getanswer(self):
        if self.getstatus():
            return "Process running"
        
        self.answer = {}
            
        self.answer[DB_VULN] = []
        
       
        
        return self.answer

    def getoutput(self):
        return "running"
        
    

if __name__ == "__main__": 
    dirsearch  = reconnaissance()   
    dirsearch.run_dirsearch("http://192.168.133.177")