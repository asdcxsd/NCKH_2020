import json
from bson import json_util
from ..Function.Connect_Framework import ClassInputFramework, run_module
from .target import get_target_url

def Run(data_json):
    module_input_raw = data_json['Input']
    input_framework = ClassInputFramework()
    input_framework.Data = {
        "Target" : []
    }
    for module in module_input_raw:
        if module['module'] not in input_framework.ListModule:
            input_framework.ListModule.append(module['module'])
        if module['module'] == 'Target':
            target_id = module['_id']
            status, data = get_target_url(target_id)
            temp = json_util.dumps(data)
            data_target_id = json.loads(temp)
            data_target_id['_id'] = data_target_id['_id']["$oid"]
            input_framework.Data['Target'].append(data_target_id)
    frmFramework = run_module(input_framework)
    return True,  frmFramework
 


