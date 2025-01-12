from Framework.Framework import Framework
from copy import deepcopy
from Framework.Valueconfig import ValueStatus, Module_Priority
import json
from bson import json_util
from .Function.Connect_Database import find_data_from_db, get_data_from_db, get_data_from_db_with_process, save_result_to_db, remove_data_from_db
from .Function.Connect_Framework import ClassInputFramework, init_module, run_module
from .Input.target import get_target_url
from .Process_running import ProcessRunning
def delete_data_in_database(module_name, module_id):
    status, data = get_data_from_db(module_name, module_id)
    if status:
        try:
            temp = json_util.dumps(data)
            data_module_id = json.loads(temp)
            data_module_id['_id'] = data_module_id['_id']["$oid"]
        except Exception as e:
            raise(e)
    else: 
        return False
    if module_name == "db_process":
        for name_md in Module_Priority.keys():
            remove_data_from_db(name_md, data_module_id['_id'], "_id_process" )
        [status, data] = remove_data_from_db("db_process", data_module_id['_id'])
        if status == False: 
            raise Exception(data)
        return True
    _id_process = data_module_id['_id_process']
    for name_md in Module_Priority.keys():
        try:
            status, data = find_data_from_db(name_md, {"pre_type_module": {"$elemMatch": {"module":module_name, "_id":data_module_id['_id']}}})
            if status == False:continue
        
            temp = json_util.dumps(data)
            data_module_new_id = json.loads(temp)
            if not isinstance(data_module_new_id, list):
                data_module_new_id = [data_module_new_id]
        except Exception as e:
            raise(e)
        for index, data_out in enumerate(data_module_new_id):
            #data_module_id[index]['_id'] = data_out['_id']["$oid"]
            try:
                delete_data_in_database(name_md, data_out['_id']["$oid"])
            except Exception as e:
                raise(e)
    [status, data] = remove_data_from_db(module_name,module_id)
    if status == False: 
        raise Exception(data)
    for name_md in Module_Priority.keys():
        status, data = find_data_from_db(name_md, {"_id_process": _id_process})
        if status == True:
            return True
    [status, data] = remove_data_from_db("db_process", _id_process)
    if status == False: 
        raise Exception(data)
    return True


def find_module_run_with_process_id(process_id):
    listkey  = list(Module_Priority.keys())
    for i in range(len(listkey)-1, 0, -1):
        name_module =listkey[i]
        status, data = get_data_from_db_with_process(name_module, process_id)
        if status:
            temp = json_util.dumps(data)
            data_module_id = json.loads(temp)
            data_module_id['_id'] = data_module_id['_id']["$oid"]
            return {"module": name_module, "_id" : data_module_id['_id']}
        return {}
def dump_all_data_from_db(module_name, module_id):
    status, data = get_data_from_db(module_name, module_id)
    if status == False: 
        return {}
    temp = json_util.dumps(data)
    data_module_id = json.loads(temp)
    data_module_id['_id'] = data_module_id['_id']["$oid"]
    if "pre_type_module" in data_module_id:
        data_reader = data_module_id['pre_type_module']
        for module_child  in  data_reader:
            try:
                if not module_child['module'] in Module_Priority.keys():
                    continue
                update_data = dump_all_data_from_db(module_child['module'], module_child['_id'])
                data_module_id.update(update_data)
            except : 
                pass
    return data_module_id
class RunFrammework():
    def __init__(self):
        self.stop_from_user = False
        self.frmFramework = init_module()
    def change_priority(self, data, config):
        new_data = deepcopy(data)
        for item in data.keys():
            if item in config.keys():
                if (item == "EXPLOIT_POCS"):
                    name_POC = config[item]['POC']
                    for id in range(len(data[item])):
                        if data[item][id]['app_name'] == name_POC:
                            new_data[item] = [data[item][id]]
                            break
                if (item == "EXPLOIT_METASPLOIT_AI"):
                    name_MTAI = config[item]['METASPLOIT']
                    for id in range(len(data[item])):
                        if data[item][id]['prod_name'] == name_MTAI:
                            new_data[item] = [data[item][id]]
                            break
        return new_data
        
    def Run(self, proRunning, data_json):
        self.stop_from_user = False
        target = ""
        module_input_raw = data_json['Input']
        priority = {}
        if "Priority" in data_json: 
            priority = data_json['Priority']
        input_framework = ClassInputFramework()
        input_framework.ListModule = data_json['Module']
        input_framework.Data = {
        }
        module_input_temp = module_input_raw.copy()
        for module in module_input_temp:
            module_id = module['_id']
            if module['module'] == "db_process":
                data  = find_module_run_with_process_id(module_id)
                if data == {}:
                    continue
                module_input_raw.append(data)
        for module in module_input_raw:
            module_id = module['_id']
            data_module_id = dump_all_data_from_db(module['module'], module_id)
            if priority != {}:
                data_module_id = self.change_priority(data_module_id, priority)
            if module['module'] == 'Target':
                #-- update target
                target = data_module_id['ip_address']
                if target == "" or target == None:
                    target = data_module_id['domain']
                #-- update target
            elif not module['module'] == 'ConfigSetup':
                target = "NoName"
                try:
                    if len(data_module_id['IN_NAME']) > 0:
                        target = data_module_id['IN_NAME'][0]
                    if len(data_module_id['IN_DOMAIN']) > 0:
                        target = data_module_id['IN_DOMAIN'][0]
                    if len(data_module_id['IN_IP']) > 0:
                        target = data_module_id['IN_IP'][0]
                
                except:
                    pass
            #set config module 
            if module['module'] == "ConfigSetup":
                input_framework.Config.update(data_module_id)
            else: 
                if not module['module'] in input_framework.Data:
                    input_framework.Data[module['module']] = {}
                for key, value in data_module_id.items():
                    if not isinstance(value, list):
                        value = [value]
                    if key not in input_framework.Data[module['module']].keys():
                        input_framework.Data[module['module']][key] = value
                    else:
                        if not isinstance(input_framework.Data[module['module']][key], list):
                            input_framework.Data[module['module']][key] = [input_framework.Data[module['module']][key]]
                        input_framework.Data[module['module']][key].extend(value)


        #-- make prcess 
        proRunning.update_infomation(target=target)
        proRunning.update_module_run(module=data_json['Module'])
        #--

        try:#change status to status running
            proRunning.change_status(ValueStatus.Running)
            
            run_module(self.frmFramework, input_framework)
            proRunning.stop_run()
            proRunning.change_status(self.frmFramework.get_status())
            print("Run process success")
            save_result_to_db(self.frmFramework.get_result().Data, proRunning.to_json(), data_json)
            print("Save to database success")
        except Exception as e:
            print("Error running framework", e)
            proRunning.change_status(ValueStatus.Error)
    def Stop(self):
       
        try:
            self.stop_from_user= True
            self.frmFramework.Stop()
           
        except Exception as e:
            print(e)
            return False
        return True
    
    def import_tool(self, namefile):
        try:
            self.frmFramework.import_tool(namefile)
            return True
        except Exception as e:
            return False
    def remove_tool(self, namefile):
        try:
            self.frmFramework.remove_tool(namefile)
            return True
        except Exception as e:
            return False