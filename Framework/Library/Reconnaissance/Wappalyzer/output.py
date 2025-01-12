from urllib.parse import urlparse
from Framework.Library.InOut_Module import OutputModuleSample
import copy
import re, string
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
    

    def add_recon_technology(self, data):
    #field: 
    #name:
    #version:
    #host:
    #summary:
        dataans = []
        tempans = {}
        #-getname
        data['referer'] = "Wappalyzer"
        host = urlparse(list(data['urls'].keys())[0])       
        if host.port == None:
            if host.scheme == "http": tempans['port'] =  80
            elif host.scheme == "https": tempans['port'] =  443
            elif host.scheme == "ssh": tempans['port'] =  22
            else: tempans['port'] = 0
        else: tempans['port'] = host.port
        for technolo in data['technologies']:
        
            try:
                insert_data = copy.deepcopy(tempans)
                insert_data['name']= technolo['name'] 
                insert_data['version']= technolo['version'] if technolo['version'] != None else ""
                insert_data['product'] = [typeTech['name'] for typeTech in technolo['categories']]
                #insert_data['summary'] =  [technolo]
                dataans.append(insert_data)
            except Exception as e:
                print("Error data wappalyzer", e)

       
        #
        for i in range(len(dataans)):
            try:
                exist = False
                for index, tech in enumerate(self.RECON_TECHNOLOGY):
                    if self.compare_string_name(tech['name'] , dataans[i]['name']) and tech['port'] ==  dataans[i]['port']:
                        
                        if tech['version'] ==  dataans[i]['version']:
                            exist = True
                            self.RECON_TECHNOLOGY[index]['summary'].append(dataans[i]['summary'])
                            break
                        if tech['version'] == "" and   dataans[i]['version'] != "":
                            self.RECON_TECHNOLOGY[index] =  dataans[i]
                            exist = True
                            break
                        if tech['version'] != "" and   dataans[i]['version'] == "": 
                            exist = True
                if exist == False:
                    self.RECON_TECHNOLOGY.append(dataans[i])
            except Exception as e:
                print("Error output wappalyzer", e)
    def compare_string_name(self, string1, string2):
        string1 = string1.lower()
        string2 = string2.lower()
        if (len(string1) != len(string2)):
            return False
        for i in range(len(string1)):
            if string1[i] in  string.ascii_letters + string.digits and string1[i] != string2[i]:
                return False
        return True 

