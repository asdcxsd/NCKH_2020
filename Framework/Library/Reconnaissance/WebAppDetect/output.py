from Framework.Library.InOut_Module import OutputModuleSample


class ModuleOutput(OutputModuleSample):


    RECON_WEBAPP = []

    def __init__(self):
        self.RECON_WEBAPP = []

        pass
    def to_json(self):
        data_json = {
            "RECON_WEBAPP": self.RECON_WEBAPP
        }
        return data_json

