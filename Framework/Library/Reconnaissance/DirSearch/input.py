from Framework.Library.InOut_Module import InputModuleSample
from Framework.Library.Function_main import freeze
class ModuleInput(InputModuleSample):
    IN_DOMAIN = []
    IN_IP = []
    IN_AUTHEN  = []
    RECON_WEBAPP  = []
    def __init__(self):
        self.IN_IP = []
        self.IN_AUTHEN = []
        self.IN_DOMAIN = []
        self.RECON_WEBAPP  = []


    def try_parse(self, data_json):
        try:
            if "IN_IP" in data_json: self.IN_IP = data_json['IN_IP']
            if "IN_DOMAIN" in data_json: self.IN_DOMAIN = data_json['IN_DOMAIN']
            if "IN_AUTHEN" in data_json: self.IN_AUTHEN = data_json['IN_AUTHEN']
            if "RECON_WEBAPP" in data_json: self.RECON_WEBAPP = data_json['RECON_WEBAPP']

        except Exception as e:
            print("Error input dirsearch", e)
            return False
        return True

    def to_json(self):
        data_json = {
            "IN_IP"    :    self.IN_IP,
            "IN_DOMAIN"        : self.IN_DOMAIN,
            "IN_AUTHEN"          : self.IN_AUTHEN,
            "RECON_WEBAPP"        : self.RECON_WEBAPP
            
        }
        return data_json
    def default_format(self):
        data_json = {
            "IN_IP"    :    self.IN_IP,
            "IN_DOMAIN"        : self.IN_DOMAIN,
            "IN_AUTHEN"          : self.IN_AUTHEN,
            "RECON_WEBAPP"        : self.RECON_WEBAPP
        }
        return data_json
    
    def extend(self, object):
        self.IN_IP.extend(object.IN_IP)
        try: self.IN_DOMAIN.extend(object.IN_DOMAIN)
        except : pass
        try: self.IN_AUTHEN.extend(object.IN_AUTHEN)
        except : pass
        try: self.RECON_WEBAPP.extend(object.RECON_WEBAPP)
        except : pass
        self.remove_duplicate()
    def remove_duplicate(self):
        self.IN_IP = freeze(self.IN_IP)
        self.IN_DOMAIN = freeze(self.IN_DOMAIN)
        self.IN_AUTHEN = freeze(self.IN_AUTHEN)
        self.RECON_WEBAPP = freeze(self.RECON_WEBAPP)