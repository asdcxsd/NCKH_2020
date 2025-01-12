#define value system 
import os
FOLDER_FRAMEWORK_ROOT =  os.path.abspath(os.path.dirname(__file__)) + "/"

#define module

Module_INPUT  = "Module_Input"
Module_RECONNAISSANCE = "Module_Reconnaissance"
Module_EXPLOIT  = 'Module_Exploit'
Module_OUTPUT = 'Module_Output'
Module_OTHER = 'Module_Other' 

Module_Priority = {
    Module_OTHER : -1,  #auto run ->> 
    Module_INPUT : 0,
    Module_RECONNAISSANCE : 1,
    Module_EXPLOIT : 2,
    Module_OUTPUT: 3
}
# adđ new type module
FORMATTIME = "%d/%m/%YT%H:%M:%S"

# read type tool input/output for module
def read_inout_for_module_framework():
    data_text = open(FOLDER_FRAMEWORK_ROOT + "Valueconfig.json").read()
    import json
    data_json = json.loads(data_text)
    data_inout_framework = data_json['Select_INOUT']


class ValueStatus():
    Running = "StatusRunning"
    Loading = "StatusLoading"
    Success = "StatusSuccess"
    Error   = "StatusError"
    Watting = "StatusWatting"
    Stop    = "StatusStop"
    Stopping= "StatusStopping"
    Start   = "StatusStart"
    Init    = "StatusInit"
    Unknow  = "StatusUnknow"
    Creating= "StatusCreating"