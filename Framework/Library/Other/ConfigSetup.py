from Framework.Library.Function_main import read_data_json_from_file
from Framework.Library.Module import Module
class ModuleFramework(Module):
    Config_value_default = {}
    def __init__(self):
        self.Config_value_default = read_data_json_from_file("Library/Module.json")['ValueConfig']
        for config in self.Config_value_default.values():
            setattr(self, config, "")
    def info(self):
        result = {}
        result['name'] = 'ConfigSetup'
        result['typemodule'] = "Module_Other"
        result['type'] = "offline"
        result['version'] = "1.0"
        return result
    def try_parse(self, data):
        for key in data.keys():
            if key in self.Config_value_default.values():
                setattr(self, key, data[key])
    def to_json(self):
        result = {}
        attrs = self.__dict__
        for key in attrs.keys():
            if key in self.Config_value_default.values():
                result[key] = attrs[key]
        return result
    def default_form(self):
        result = {}
        attrs = self.__dict__
        for key in attrs.keys():
            if key in self.Config_value_default.values():
                result[key] = attrs[key]
        return result
class ModuleInput():
    pass
class ModuleOutput():
    pass