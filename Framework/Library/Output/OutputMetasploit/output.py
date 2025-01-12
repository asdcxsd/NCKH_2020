from Framework.Library.InOut_Module import OutputModuleSample

from datetime import datetime
class ModuleOutput(OutputModuleSample):

    Cf_Server_OpenPort = ""
    id_connect = ""
    date_connect = ""
    target_connect = ""
    ip_reverse_shell = ""
    port_reverse_shell = ""
    status  = ""
    OUTPUT_LOG_RUN_SHELL = []

    def __init__(self):
        self.OUTPUT_LOG_RUN_SHELL = []
        self.Cf_Server_OpenPort = ""
        self.id_connect = ""
        self.date_connect = ""
        self.target_connect = ""
        self.ip_reverse_shell = ""
        self.port_reverse_shell = ""
        self.status  = ""
        pass
    def make_config_connect(self, server_rev, ip_rev, port_rev):
        self.Cf_Server_OpenPort = server_rev
        self.ip_reverse_shell = ip_rev
        self.port_reverse_shell = port_rev
    def update_status(self,target, status, id_connect='No'):
        self.target_connect = target
        self.status = status
        self.id_connect = id_connect
        dateTimeObj = datetime.now()
        from Framework.Valueconfig import FORMATTIME # FORMATTIME = "%d/%m/%YT%H:%M:%S"
        self.date_connect = dateTimeObj.strftime(FORMATTIME)
    def to_json(self):
        result = {
            "Server_REV" : self.Cf_Server_OpenPort,
            "id_connect" : self.id_connect,
            "date_connect": self.date_connect,
            "target_connect": self.target_connect,
            "ip_reverse_shell": self.ip_reverse_shell,
            "port_reverse_shell":self.port_reverse_shell,
            "status": self.status 
        }
        self.OUTPUT_LOG_RUN_SHELL= [result]
        data_json = {
            "OUTPUT_LOG_RUN_SHELL": self.OUTPUT_LOG_RUN_SHELL
        }
        return data_json


