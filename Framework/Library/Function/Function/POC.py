from Framework.Library.Function_main import get_info_of_tool
from Framework.Library.Function.Function.PocSuite.api import start_pocsuite
import threading
import time
from Framework.Valueconfig import ValueStatus
import random, string
from Framework.Library.Function.Function.PocSuite.PocSuite3_API import get_all_class_tool, check_result, createScan, get_infomation_of_tool
#only one target 
class POC(): 
    Config = {}
    Input_framework = {}
    PoCs_Select = []
    List_tool_have_to_run = []
    URL = {}
    MODE = "attack"

    #result = 
    Result = []
    def __init__(self):
        self.PoCs_Select = get_all_class_tool()
        self.List_tool_have_to_run = []
        self.Result = []
        pass
    def func_thread_update_status(self):
        while True:
            for poc in self.PoCs_Select:
                ans = check_result(self.URL,poc, self.MODE)
                if len(ans) == 0:
                    continue
                for an in ans:
                    if an[0] == True: 
                        self.Result.append(an[1])
                        poc_run = poc
                    else: poc_run = an[1]
                    for id_status in range(len(self.StatusOfTool)):
                        if self.StatusOfTool[id_status]['name'] == poc_run:
                            self.StatusOfTool[id_status]['status'] = ValueStatus.Success
            if self.get_status() == ValueStatus.Success or self.get_status() == ValueStatus.Error:
                break
            time.sleep(1)
    def run(self):
        self.URL = "http://" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + ".vn"
        data_input = {
            "Config": self.Config,
            "Input" : self.Input_framework.to_json()
        }
        createScan(self.URL, self.PoCs_Select, mode=self.MODE,  data=data_input)
        start_pocsuite()
        self.StatusOfTool = [{'name': name, 'status':ValueStatus.Running} for name in  self.PoCs_Select]
        thread  = threading.Thread(target=self.func_thread_update_status, args=())
        thread.start()
        pass
    def get_status(self):
        for id_status in range(len(self.StatusOfTool)):
            if not (self.StatusOfTool[id_status]['status'] == ValueStatus.Success or self.StatusOfTool[id_status]['status'] == ValueStatus.Error) :
                return ValueStatus.Running
        return ValueStatus.Success

    def set_input(self, input):
        
        self.Input_framework = input
    def fillter_tools(self):
        list_tool = get_all_class_tool()
        list_old_poc = self.PoCs_Select
        self.PoCs_Select = []
        for poc in list_old_poc:
            if self.compare_tool(poc):
                self.PoCs_Select.append(poc)

        for poc in self.List_tool_have_to_run:
            if not poc in self.PoCs_Select:
                self.PoCs_Select.append(poc)
    def compare_tool(self, name_poc): ## check fake
        info = get_infomation_of_tool(name_poc)
        return True
    def set_config(self, data):
        self.List_tool_have_to_run = data['Cf_List_Tool_CheckPocs_Have_To_Run']
        self.Config = data

    def result(self):
        return self.Result


#class manager 
    def get_all_pocs(self):
        return get_all_class_tool()
    def get_info_poc(self, name_poc):
        return get_infomation_of_tool(name_poc)