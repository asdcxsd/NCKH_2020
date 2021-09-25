from Framework.Library.InOut_Module import OutputModuleSample


class ModuleOutput(OutputModuleSample):


    RECON_SERVICES = []
    RECON_PORTS = []
    RECON_OS  = []

    def __init__(self):
        self.RECON_SERVICES = []
        self.RECON_PORTS = []
        self.RECON_OS = []
        pass
    def to_json(self):
        data_json = {
            "RECON_SERVICES": self.RECON_SERVICES,
            "RECON_PORTS"   : self.RECON_PORTS,
            "RECON_OS"      :self.RECON_OS
        }
        return data_json

