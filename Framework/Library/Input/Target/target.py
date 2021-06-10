from Framework.Library.Function_main import compare_field, check_in_list
from Framework.Library.Module import Module
from Framework.Library.Input.Target.input import ModuleInput
from Framework.Library.Input.Target.output import ModuleOutput
from Framework.Valueconfig import ValueStatus
class ModuleFramework(Module):
    name = "Target"
    path_input_class = "/input.py"
    path_output_class = "/output.py"
    input_module = None
    input_data = []
    status = ''
    def __init__(self):
        self.input_data = []
        pass
    
    def start(self):
        self.status = ValueStatus.Running
        try:
            if "Target" not in self.input_data: 
                self.status = ValueStatus.Success
                return 
            output_result = ModuleOutput()
            for data_input in self.input_data['Target']:
                input_class= ModuleInput()
                input_class.try_parse(data_input)
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
        if not check_in_list(outputObject.IN_AUTHEN, inputObjectTarget.authen, type_compare="delete_null"):
            outputObject.IN_AUTHEN.append(inputObjectTarget.authen)
        if not check_in_list(outputObject.IN_DESCRIBE, inputObjectTarget.describe, type_compare="delete_null"):
            outputObject.IN_DESCRIBE.append(inputObjectTarget.describe)
        if not check_in_list(outputObject.IN_DOMAIN, inputObjectTarget.domain, type_compare="delete_null"):
            outputObject.IN_DOMAIN.append(inputObjectTarget.domain)
        if not check_in_list(outputObject.IN_IP, inputObjectTarget.ip_address, type_compare="delete_null"):
            outputObject.IN_IP.append(inputObjectTarget.ip_address)
        if not check_in_list(outputObject.IN_NAME, inputObjectTarget.name, type_compare="delete_null"):
            outputObject.IN_NAME.append(inputObjectTarget.name)


        return outputObject
