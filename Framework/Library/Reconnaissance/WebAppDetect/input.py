from Framework.Library.InOut_Module import InputModuleSample

class ModuleInput(InputModuleSample):
    IN_DOMAIN = []
    IN_IP = []
    RECON_PORTS = []
    def __init__(self):
        self.IN_IP = []
        self.IN_DOMAIN = []
        self.RECON_PORTS = []
    def try_parse(self, data_json):
        try:
            if "IN_IP" in data_json: self.IN_IP = data_json['IN_IP']
            if "IN_DOMAIN" in data_json: self.IN_DOMAIN = data_json['IN_DOMAIN']
            if "RECON_PORTS" in data_json: self.RECON_PORTS = data_json['RECON_PORTS']
        except Exception as e:
            print("Error input web detect:", e)
            return False
        return True

    def to_json(self):
        data_json = {
            "IN_IP"    :    self.IN_IP,
            "IN_DOMAIN"        : self.IN_DOMAIN,
            "RECON_PORTS"        : self.RECON_PORTS
            
        }
        return data_json
    def default_format(self):
        data_json = {
            "IN_IP"    :    self.IN_IP,
            "IN_DOMAIN"        : self.IN_DOMAIN,
            "RECON_PORTS"        : self.RECON_PORTS
            
        }
        return data_json
    def extend(self, object):
        self.IN_IP.extend(object.IN_IP)
        self.IN_DOMAIN.extend(object.IN_DOMAIN)
        self.RECON_PORTS.extend(object.RECON_PORTS)
        self.remove_duplicate()
    def remove_duplicate(self):
        self.IN_IP = list(set(self.IN_IP))
        self.IN_DOMAIN = list(set(self.IN_DOMAIN))
        self.RECON_PORTS = list(set(self.RECON_PORTS))