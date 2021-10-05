from Framework.Library.InOut_Module import InputModuleSample

class ModuleInput(InputModuleSample):
    IN_DOMAIN = []
    IN_IP = []
    IN_AUTHEN  = []
    def __init__(self):
        self.IN_IP = []
        self.IN_AUTHEN = []
        self.IN_DOMAIN = []


    def try_parse(self, data_json):
        try:
            if "IN_IP" in data_json: self.IN_IP = data_json['IN_IP']
            if "IN_DOMAIN" in data_json: self.IN_DOMAIN = data_json['IN_DOMAIN']
            if "IN_AUTHEN" in data_json: self.IN_AUTHEN = data_json['IN_AUTHEN']

        except Exception as e:
            print("Error input dirsearch", e)
            return False
        return True

    def to_json(self):
        data_json = {
            "IN_IP"    :    self.IN_IP,
            "IN_DOMAIN"        : self.IN_DOMAIN,
            "IN_AUTHEN"          : self.IN_AUTHEN
            
        }
        return data_json
    def default_format(self):
        data_json = {
            "IN_IP"    :    self.IN_IP,
            "IN_DOMAIN"        : self.IN_DOMAIN,
            "IN_AUTHEN"          : self.IN_AUTHEN
        }
        return data_json