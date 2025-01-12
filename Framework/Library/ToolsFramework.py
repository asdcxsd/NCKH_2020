
from os import remove
from sys import flags
from .Function_main import read_data_json_from_file, get_info_of_tool, get_class_module
from ..Valueconfig import FOLDER_FRAMEWORK_ROOT, ValueStatus
from .Module import Module, Status
from .InOut_Framework import OutputFramework

import threading
class ToolsFramework():
    input_module = None
    output_module = None

    list_tools = []
    Status = []
    status_error = ''
    type = "" # default of type tool
    def __init__(self, type):
        self.type=type
        self.output_module = OutputFramework(self.type)
        self.output_module.Data = {
            self.type : {}
        }
        self.input_module = None
        self.list_tools = []
        self.Status = []
        self.status_error = ''
    def run_object_tool_thread(self, object_tool, Id_tool):
        object_tool.set_config_module(self.input_module.Config)
        object_tool.set_input_module(self.input_module.Data)
        object_tool.update_result_process_session(self.list_tools, self.Status, self.output_module)
        #object_tool.start()
        def start_local(object_tool_local):
            object_tool_local.start()
        thred = threading.Thread(target=start_local, args=(object_tool,)).start()
        status = False
        while (True):
            try:
                if self.Status[Id_tool].getStatus() == ValueStatus.Stopping:
                    object_tool.stop();
                    status = False   
                    break
                self.Status[Id_tool].running()
                self.Status[Id_tool].set_output(object_tool.output())
                
                if object_tool.get_status() == ValueStatus.Success:
                    status = True
                    break
                if object_tool.get_status() == ValueStatus.Error:
                    status = False   
                    break
                    
            except  Exception as e:
                status = False
                break
        self.output_module.update_list(object_tool.get_output_module())
        if status:
            self.Status[Id_tool].success()
        else:
            self.Status[Id_tool].error()
        del object_tool
    def start(self): # run thread 
        import sys
        for Id_tool in range(len(self.list_tools)):
            try:
                tool = self.list_tools[Id_tool]

                nameModuleJson = get_info_of_tool(tool)
                pathMain = nameModuleJson['PathMain']
                [status, classModule, classInput, classOutput] = get_class_module(pathMain)
                try:
                    object_tool = classModule()
                except:
                    print("Class module fail: ", str(classModule))
                    raise Exception("Class error")
                thread = threading.Thread(target=self.run_object_tool_thread, args=(object_tool, Id_tool, ))
                thread.start()
                self.Status[Id_tool].set_thread(thread)
                del object_tool
            except Exception as e:
                print("Exception error run tools", e)
                self.Status[Id_tool].error()
    def stop(self): # get status  running
        for i in self.Status:
            i.set_stop();
        pass
    def get_status(self): # get status  running
        for i in self.Status:
            if i.getStatus() != ValueStatus.Error  and i.getStatus() != ValueStatus.Success:
                return ValueStatus.Running
        return ValueStatus.Success
        pass

    def get_all_tools(self):

        json_data = read_data_json_from_file("Library/Module.json")
        modules= json_data['Module']
        ans = []
        for module in modules:
            if module['TypeModule'] == self.type or self.type == 'all':
                ans.append(module['NameModule'])
        return ans
    def get_info_tool(self, name_tool):
        json_data = read_data_json_from_file("Library/Module.json")
        modules= json_data['Module']
        ans  = None
        for module in modules:
            if module['NameModule'] == name_tool:
                ans = module
        return ans
    def set_tools(self, tool, control='add'):
        #check tool in framework
        tools = self.get_all_tools()
        if tool not  in tools:
            self.status_error += ("| add tool error: tool not in framework ")
            return False
        if control == 'add':
            if tool in self.list_tools:
                self.status_error += ("| add tool error: tool exist ")
                return False
            self.list_tools.append(tool)
            #add class input, output 
            json_data = read_data_json_from_file("Library/Module.json")
            modules= json_data['Module']
            index_of_tool = [module['NameModule'] for module in modules].index(tool)
            self.Status.append(Status(modules[index_of_tool]))

        elif control == 'remove':
            remove_success = False
            for index_tool in range(len(self.list_tools)):
                if self.list_tools[index_tool] == tool:
                    self.list_tools.pop(index_tool)
                    self.status.pop(index_tool)
                    remove_success = True
            if not remove_success: 
                self.status_error.append("| remove tool error: tool don't exist ")
                return False
        return True
    def get_priority(self):
        from Framework.Valueconfig import Module_Priority
        return Module_Priority[self.type]
    def set_input_module(self, input):
        self.input_module = input
    def result(self):
        return self.output_module