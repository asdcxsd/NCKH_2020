from Framework.Valueconfig import ValueStatus
from Framework.Library.InOut_Module import OutputModuleSample

from datetime import datetime
class ModuleOutput(OutputModuleSample):
    OUTPUT_REPORT_PDF = []

    def __init__(self):
        self.OUTPUT_REPORT_PDF = []
    def to_json(self):
        data_json = {
            "OUTPUT_REPORT_PDF": self.OUTPUT_REPORT_PDF
        }
        return data_json


