from Framework.Library.InOut_Module import OutputModuleSample


class ModuleOutput(OutputModuleSample):
    IN_DOMAIN = []
    IN_IP = []
    IN_AUTHEN  = []
    IN_NAME = []
    IN_DESCRIBE = []
    def __init__(self):
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