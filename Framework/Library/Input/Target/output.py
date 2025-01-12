from Framework.Library.Function_main import freeze
from Framework.Library.InOut_Module import OutputModuleSample


class ModuleOutput(OutputModuleSample):
    IN_DOMAIN = []
    IN_IP = []
    IN_AUTHEN  = []
    IN_NAME = []
    IN_DESCRIBE = []
    def __init__(self):

        self.IN_DOMAIN = []
        self.IN_IP = []
        self.IN_AUTHEN  = []
        self.IN_NAME = []
        self.IN_DESCRIBE = []
        pass
    
    def to_json(self):
        data_json = {
            "IN_IP"    :    self.IN_IP,
            "IN_DOMAIN"        : self.IN_DOMAIN,
            "IN_DESCRIBE"          : self.IN_DESCRIBE,
            "IN_NAME"          : self.IN_NAME,
            "IN_AUTHEN"          : self.IN_AUTHEN,
            
        }
        return data_json
    def remove_duplicate(self):
        self.IN_IP = freeze(self.IN_IP)
        self.IN_DOMAIN = freeze(self.IN_DOMAIN)
        self.IN_DESCRIBE = freeze(self.IN_DESCRIBE)
        self.IN_NAME = freeze(self.IN_NAME)
        self.IN_AUTHEN = freeze(self.IN_AUTHEN)
