from Framework.Library.Function_main import compare_field, check_in_list
from Framework.Library.Module import Module
from Framework.Library.Input.Target.input import ModuleInput
from Framework.Library.Input.Target.output import ModuleOutput
from Framework.Valueconfig import ValueStatus
import socket
class ModuleFramework(Module):
    name = "Target"
    type_module = "Module_Input"
    path_input_class = "/input.py"
    path_output_class = "/output.py"
    input_module = None
    input_data = []
    status = ''
    def __init__(self):
        self.input_data = []
        pass
    def info(self):
        result = {}
        result['name'] = self.name
        result['typemodule'] = self.type_module
        result['type'] = "offline"
        result['version'] = "2.0"
        return result
    def start(self):
        self.status = ValueStatus.Running
        try:
            if "Target" not in self.input_data: 
                self.status = ValueStatus.Success
                return 
            output_result = ModuleOutput()

            input_class= ModuleInput()
            input_class.try_parse(self.input_data['Target'])
            if input_class.domain != [] and input_class.domain[0] != "":
                try:
                    ip = socket.gethostbyname(input_class.domain[0])
                    input_class.ip_address = [ip]
                except:
                    pass
            output_result = self.add_data_to_object_output(input_class, output_result)
            self.output_module = output_result
            self.status = ValueStatus.Success
        except Exception as e:
            self.status = ValueStatus.Error

    def get_status(self):
        return self.status
    def set_input_module(self, input):
        self.input_data = input
    def get_output_module(self):
        return self.output_module
        
    def add_data_to_object_output(self, inputObjectTarget, outputObject):
        outputObject.IN_AUTHEN.extend(inputObjectTarget.authen)
        outputObject.IN_DESCRIBE.extend(inputObjectTarget.describe)
        outputObject.IN_DOMAIN.extend(inputObjectTarget.domain)
        outputObject.IN_IP.extend(inputObjectTarget.ip_address)
        outputObject.IN_NAME.extend(inputObjectTarget.name)
        outputObject.remove_duplicate()
        return outputObject
