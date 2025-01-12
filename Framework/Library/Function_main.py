
from Framework.Valueconfig import FOLDER_FRAMEWORK_ROOT
import json

def sort_module_framework_by_priority(arrModule = []):
  
    sorted(arrModule,key=lambda module: module.get_priority())
    return  arrModule


def read_data_json_from_file(path):
    with  open(FOLDER_FRAMEWORK_ROOT + path) as file:
        data_text = file.read()
    data_json = json.loads(data_text)

    return data_json

def write_data_json_to_file(path, data):
    try:
        data_text = json.dumps(data)
        with open(FOLDER_FRAMEWORK_ROOT + path, "w") as file:
            file.write(data_text)
        return True
    except Exception as e:
        return False

def import_file_from_name(paths, root = "Library"):
    if root ==  "Library":
        paths =  FOLDER_FRAMEWORK_ROOT +  root + paths
    import importlib
    spec = importlib.util.spec_from_file_location("module.name", paths) 
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo


def  get_class_module(path):
    try:
        class_tool = import_file_from_name(path)
        return [True, class_tool.ModuleFramework, class_tool.ModuleInput, class_tool.ModuleOutput]
    except Exception as e:
        return [False, str(e), None, None]
def  get_info_of_tool(name_module):
    from Framework.Library.ToolsFramework import ToolsFramework
    toolFrame = ToolsFramework('all')
    ans = toolFrame.get_info_tool(name_module)
    return ans

def compare_field(field1, field2, type_compare=""):
    if field1 == field2:
        return True
    if isinstance(field1, str) and isinstance(field2, str):
        return field1.lower() == field2.lower()
    return False

def check_in_list(lists, value, type_compare=''):
    if type_compare == 'delete_null':
        if value == '' or value == None or value == []:
            return True
    for value_list in lists:
        if compare_field(value_list, value, type_compare):
            return True
    return False


def freeze(l):
    if not isinstance(l, list):
        return l
    answer = []
    for d in l:
        if not d in answer: 
            answer.append(d)
    return answer
def remove_duplicate( data_input):
    for key in data_input.keys():
        for chid_key in data_input[key].keys():
            data_input[key][chid_key]  = freeze(data_input[key][chid_key])
    return data_input