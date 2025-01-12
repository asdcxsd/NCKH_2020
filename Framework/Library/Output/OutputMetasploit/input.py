from Framework.Library.InOut_Module import InputModuleSample

class ModuleInput(InputModuleSample):
    EXPLOIT_POCS = []
    EXPLOIT_METASPLOIT_AI = []
    def __init__(self):
        self.EXPLOIT_POCS = []
        self.EXPLOIT_METASPLOIT_AI = []

    def try_parse(self, data_json):
        try:
            if "EXPLOIT_POCS" in data_json:
                self.EXPLOIT_POCS = data_json['EXPLOIT_POCS']

            if "EXPLOIT_METASPLOIT_AI" in data_json:
                self.EXPLOIT_METASPLOIT_AI =data_json['EXPLOIT_METASPLOIT_AI']

        except Exception as e:
            print("Error read data metasploitAI", e)
            return False
        return True

    def to_json(self):
        data_json = {
            "EXPLOIT_POCS"    :    self.EXPLOIT_POCS,
            "EXPLOIT_METASPLOIT_AI": self.EXPLOIT_METASPLOIT_AI,
        }
        return data_json
    def default_format(self):
        data_json = {
            "EXPLOIT_POCS"    :    self.EXPLOIT_POCS,
            "EXPLOIT_METASPLOIT_AI": self.EXPLOIT_METASPLOIT_AI,

        }
        return data_json
    def freeze(self, l):

        answer = []
        for d in l:
            if not d in answer: 
                answer.append(d)
        return answer

    def extend(self, object):
        self.EXPLOIT_POCS.extend(object.EXPLOIT_POCS)
        self.EXPLOIT_METASPLOIT_AI.extend(object.EXPLOIT_METASPLOIT_AI)
        self.remove_duplicate()
    def remove_duplicate(self):
        self.EXPLOIT_POCS = self.freeze(self.EXPLOIT_POCS)
        self.EXPLOIT_METASPLOIT_AI = self.freeze(self.EXPLOIT_METASPLOIT_AI)