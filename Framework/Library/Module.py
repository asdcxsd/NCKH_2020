#define module
class Module():
    input_module = None
    output_module = None
    config_module = None
    list_tools = []
    def __init__(self):
        pass
    def info(self):
        return {
            "name" : "Unknow",
            "typemodule" : "Module_Other",
            "type" : "Unknow"
        }
    def set_input_module(self, input):
        self.input_module = input
    def set_config_module(self, config):
        self.config_module = config

    def get_output_module(self):
        return self.output_module
    def set_output_module(self, input):
        pass

    def start(self):
        pass
    def get_status(self):
        pass
    def update_result_process_session(self, listtools,liststatus,  list_result):
        pass
    def output(self):
        return None
from Framework.Valueconfig import ValueStatus
class Status():
    string_output = ""
    answer  = None
    Thread = None
    status  = "unknow"
    module = ""
    def __init__(self, module):
        self.module = module
        pass
    def running(self):
        self.status  = ValueStatus.Running
    def end(self):
        self.status = ValueStatus.Success
    def watting(self):
        self.status = ValueStatus.Watting
    def success(self):
        self.status = ValueStatus.Success
    def error(self):
        self.status = ValueStatus.Error
    def getStatus(self):
        return self.status
    def set_output(self, string):
        if not string == None:
            self.string_output += string
    def set_thread(self, thread):
        self.Thread = thread
    
