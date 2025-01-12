
class Module_Framework():
    type_module = "None"
    object_module = None # save main object
    output_module = None # Output save when success
    input_module = None # input
    def __init__(self, name_type, object_module):
        self.type_module = name_type
        self.object_module = object_module
    def get_priority(self):
        from Framework.Valueconfig import Module_Priority
        return Module_Priority[self.type_module]
    def start(self):
        if self.input_module == None:
            raise Exception("Input is null")
        self.object_module.set_input_module(self.input_module)
        self.object_module.start()
        self.output_module = self.object_module.get_output_module()

class ModuleStatus():
    isRunning = False
    isStart = False
    isStop = False
    isSuccess = False
    errorText = ""
    listThread = []
    def __init__(slef):
        pass
    def get(self):
        return  self.data
    def set(self, data):
        self.data = data