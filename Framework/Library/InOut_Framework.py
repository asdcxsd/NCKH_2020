from Framework.Library.Function_main import check_in_list, import_file_from_name, read_data_json_from_file

class InputFramework():
    Config = {}
    Data = {}
    ListModule = []
    def __init__(self):
        pass
    def try_parse(self, data_json):
        self.List_module = data_json.Config
        self.Data = data_json.Data
        self.ListModule = data_json.ListModule
        pass

    def to_json(self):
        data = {
            "Config" : self.Config ,
            "Data" : self.Data,
            "ListModule": self.ListModule
        }
    def  module_run(self):
        return self.ListModule


class OutputFramework():
    type_module = None
    List_Output = []
    Data = {}
    ValueConst = {}
    def __init__(self, type):
        self.type_module = type
        json_data = read_data_json_from_file("Library/Module.json")
        self.ValueConst = json_data['ValueOutput']
        self.Data = {
            self.type_module : {}
        }
    def try_parse(self, data_json):
        self.Data = data_json

    def to_json(self):
        return {
            "Data" : self.Data
        }
    def update_list(self, output):
        self.List_Output.append(output)
        self.merge_data_extend(output)
    def merge_data_extend(self, data):
        try:
            data = data.to_json()
        except Exception as e:
            print("Error merge Output Framewwork: ", e)
            return {}
        data_pre = self.Data[self.type_module]
        data_class = read_data_json_from_file("Library/Module.json")['ClassMergeData']
        for key in data.keys():
            if key not in data_pre.keys():
                if key in self.ValueConst.values():
                    data_pre[key] =[]
                else: continue
            if not key in data_class.keys():
                for data_key in data[key]:
                    if not check_in_list(data_pre[key], data_key):
                        data_pre[key].append(data_key)
                continue
            file_class = data_class[key]
            classMerges = import_file_from_name(file_class)
            objectMerge = classMerges.MergeData()
            data_pre[key] = objectMerge.merge_data(data_pre[key], data[key])
        self.Data = {
            self.type_module : data_pre
        }
        pass
    
    def merge_all(self):
        pass