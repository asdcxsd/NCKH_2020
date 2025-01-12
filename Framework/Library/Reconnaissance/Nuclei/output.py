from Framework.Library.InOut_Module import OutputModuleSample
import copy
import re, string
from urllib.parse import urlparse
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
        data['referer'] = "Nuclei"
        #tempans['summary'] = [data]
        host = urlparse(data['host'])       
        if host.port == None:
            if host.scheme == "http": tempans['port'] =  80
            elif host.scheme == "https": tempans['port'] =  443
            elif host.scheme == "ssh": tempans['port'] =  22
            else: tempans['port'] = 0
        else: tempans['port'] = host.port
        tempans['product'] = host.scheme
        for res in data['results']:
            try:
                insert_data = copy.deepcopy(tempans)
                insert_data['name'] = res.split('/')[0]
                
                if '/' in res:
                    insert_data['version'] = res[len(insert_data['name'])+ 1: ]
                else:
                    insert_data['version'] = res[len(insert_data['name']): ]
                dataans.append(insert_data)
            except:
                pass

        #
        for i in range(len(dataans)):
            try:
                exist = False
                for index, tech in enumerate(self.RECON_TECHNOLOGY):
                    if self.compare_string_name(tech['name'] , dataans[i]['name']) and tech['port'] ==  dataans[i]['port']:
                        
                        if tech['version'] ==  dataans[i]['version']:
                            exist = True
                            #self.RECON_TECHNOLOGY[index]['summary'].append(dataans[i]['summary'])
                            break
                        if tech['version'] == "" and   dataans[i]['version'] != "":
                            self.RECON_TECHNOLOGY[index] =  dataans[i]
                            exist = True
                            break
                if exist == False:
                    self.RECON_TECHNOLOGY.append(dataans[i])
            except Exception as e:
                print("Error output nuclei", e)

    def compare_string_name(self, string1, string2):
        string1 = string1.lower()
        string2 = string2.lower()
        if (len(string1) != len(string2)):
            return False
        for i in range(len(string1)):
            if string1[i] in  string.ascii_letters + string.digits and string1[i] != string2[i]:
                return False
        return True 
