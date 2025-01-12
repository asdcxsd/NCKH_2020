from Framework.Valueconfig import Module_Priority, ValueStatus
from .Library.Function_main import import_file_from_name, get_info_of_tool, get_class_module, remove_duplicate
import sys, copy, time
from .Library.ToolsFramework import ToolsFramework
from .Library.InOut_Framework import InputFramework, OutputFramework
from .Library.Import_Tools import import_tool, remove_tool
class Framework():
    output_framework = None
    status = None
    stop_from_user = False
    def __init__(self):
        self.output_framework = OutputFramework("Result")
        #import all class
        pass
    def get_list_of_module(self, type='all'):
        toolFrame = ToolsFramework(type)
        list_tool = toolFrame.get_all_tools()
        return list_tool
    def get_info_main_module(self, name_module):
        try:
            classmain = get_info_of_tool(name_module)['PathMain']
            status, classMain, classInput, classOutput = get_class_module(classmain)
            if status == False:
                raise Exception(classMain)
            return classMain().info()
        except Exception as e:
            return{
                "name":"Error",
                "error": str(e)
            }
        pass
    def get_class_module(self, path):# return class main, input, output
        return get_class_module(path)

    def get_info_of_module(self, name_module):
        return get_info_of_tool(name_module)
        
    #--- class inout for framework
    def get_class_input_framework(self):
        return InputFramework
    def get_class_output_framework(self):
        return OutputFramework


    def Run(self, input_run = {}, output_run = {}):
        self.stop_from_user = False
        self.status = ValueStatus.Running
        module_framework_run = input_run.ListModule
        # convert input module to type module -> run thread 
        List_type_module_run = []
        for module in module_framework_run:
            try:
                info_module = self.get_info_of_module(module)
                type_module = info_module['TypeModule']
                exist_type_module = False
                for type_exist in List_type_module_run:
                    if type_exist.type  == type_module:
                        type_exist.set_tools(module)
                        exist_type_module = True
                if exist_type_module == False:
                    List_type_module_run.append(ToolsFramework(type_module))
                    List_type_module_run[-1].set_tools(module)
            except Exception as e:
                print("Error module '", module , "':", e);

        # ->> 
        from Framework.Library.Function_main import sort_module_framework_by_priority
        module_framework_run = sort_module_framework_by_priority(List_type_module_run) # sort by priority

        # output of module is  input of other module: Input -> reconnaissance -> exploit -> output
        #select input for module
        # if input of this module is multi then  run all this -> merge output
        Input_running = input_run
        result_module_run = []
        for id_module_run in range(len(module_framework_run)):
            try:
                module_framework_run[id_module_run].set_input_module(Input_running)

                module_framework_run[id_module_run].start()
                while not (module_framework_run[id_module_run].get_status() == ValueStatus.Error or module_framework_run[id_module_run].get_status() == ValueStatus.Success):
                    
                    time.sleep(1)
                    if self.stop_from_user == True:
                        module_framework_run[id_module_run].stop()
                        raise Exception("Stop from user")
                temp = Input_running.Data
                data_new = module_framework_run[id_module_run].result().Data
                Input_running.Data = copy.deepcopy(data_new)
                for key in temp.keys():
                   
                    if key in Module_Priority:
                        for key_chid in Input_running.Data.keys():
                            try:
                                if isinstance(temp[key], list):
                                    for tem in temp[key]:
                                        Input_running.Data[key_chid].update(tem)
                                else:
                                    Input_running.Data[key_chid].update(temp[key])
                            except Exception as e:
                                print("Error json module all", e)
                Input_running.Data = remove_duplicate(Input_running.Data)
                result_module_run.append(data_new)

            except Exception as e:
                print("Error start type module all:", e)
                if self.stop_from_user == True:
                    break
        for result_module in result_module_run:
            self.output_framework.Data['Result'].update(result_module)
        self.status = ValueStatus.Success
        if self.stop_from_user == True:
            self.status = ValueStatus.Error
    def get_status(self):
        return self.status
    def get_result(self):
        return self.output_framework
    def Stop(self):
        self.stop_from_user = True

    def import_tool(self, filename):
        return import_tool(filename)
    def remove_tool(self, name_module):
        return remove_tool(name_module)