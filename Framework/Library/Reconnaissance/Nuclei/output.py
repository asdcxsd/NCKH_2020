from Framework.Library.InOut_Module import OutputModuleSample


class ModuleOutput(OutputModuleSample):


    RECON_CVE = []
    RECON_VULN = []
    RECON_SERVICES = []
    RECON_CONFIG = []
    RECON_TECHNOLOGY = []
    def __init__(self):
        self.RECON_CVE = []
        self.RECON_VULN = []
        self.RECON_SERVICES = []
        self.RECON_CONFIG = []
        self.RECON_TECHNOLOGY = []

        pass
    def to_json(self):
        data_json = {
            "RECON_CVE": self.RECON_CVE,
            "RECON_VULN": self.RECON_VULN,
            "RECON_SERVICES": self.RECON_SERVICES,
            "RECON_CONFIG": self.RECON_CONFIG,
            "RECON_TECHNOLOGY": self.RECON_TECHNOLOGY
        }
        return data_json


