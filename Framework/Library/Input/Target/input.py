from Framework.Library.InOut_Module import InputModuleSample

class ModuleInput(InputModuleSample):
    ip_address = None
    domain = None
    describe = None
    name = None
    date = None
    authen = {} # None = All
    def __init__(self):
        import random, string
        from datetime import datetime
        
        self.name = "No_Name_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        self.describe = ""
        dateTimeObj = datetime.now()
        from Framework.Valueconfig import FORMATTIME # FORMATTIME = "%d/%m/%YT%H:%M:%S"
        self.date = dateTimeObj.strftime(FORMATTIME)
        self.authen = {}
        self.domain = 'unknow'
        self.ip_address = []

    def try_parse(self, data_json):
        try:
            if ("ip_address" in data_json): self.ip_address = data_json['ip_address']
            if ("domain" in data_json): self.domain = data_json['domain']
            if ("describe" in data_json): self.describe = data_json['describe']
            if ("name" in data_json): self.name = data_json["name"]
            if ("date" in data_json): self.date = data_json["date"]
            if ("authen" in data_json): self.authen = data_json["authen"]
        except Exception as e:
            print("Error read data Target", e)
            return False
        return True

    def to_json(self):
        data_json = {
            "ip_address"    : self.ip_address,
            "domain"        : self.domain,
            "describe"      : self.describe,
            "name"          : self.name,
            "date"          : self.date,
            "authen"          : self.authen,
        }
        return data_json
    def default_format(self):
        data_json = {
            "ip_address"    : self.ip_address,
            "domain"        : self.domain,
            "describe"      : self.describe,
            "name"          : self.name,
            "date"          : self.date,
            "authen"          : self.authen,
            }
        return data_json