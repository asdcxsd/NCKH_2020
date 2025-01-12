from Framework.Library.Function_main import read_data_json_from_file
from Framework.Library.InOut_Module import InputModuleSample

class ModuleInput(InputModuleSample):
    def __init__(self):
        json_data = read_data_json_from_file("Library/Module.json")
        self.ValueConst = json_data['ValueOutput']
        self.data  = {} 

    def try_parse(self, data_json):
        try:
            self.data  = {} 
           
            for key, value in data_json.items():
                if key in self.ValueConst.values():
                    self.data[key] = value
            #list process 
           
        except Exception as e:
            print("Error output shell", e)
            return False
        return True

    def to_json(self):
        return self.data
    def default_format(self):
        data_json = {
        }
        for key in self.ValueConst.values():
            data_json[key]  = []
        return data_json
    def freeze(self, l):

        answer = []
        for d in l:
            if not d in answer: 
                answer.append(d)
        return answer

    def extend(self, object):
        for key, value in object.data.items():
            if key not in self.data.keys():
                self.data[key] = []
            self.data[key].extend(value)
        self.remove_duplicate()
    def remove_duplicate(self):
        for key, value in self.data.items():
            self.data[key] = self.freeze(value)