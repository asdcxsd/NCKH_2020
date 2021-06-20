from Framework.Library.InOut_Module import OutputModuleSample


class ModuleOutput(OutputModuleSample):
    RECON_DIR   = [] 
    RECON_FILE  = []

    def __init__(self):
        self.RECON_DIR = []
        self.RECON_FILE = []
        pass
    def to_json(self):
        data_json = {
            "RECON_DIR"     : self.RECON_DIR,
            "RECON_FILE"    : self.RECON_FILE
            
        }
        return data_json
