from Framework.Framework import Framework
ClassInputFramework = Framework().get_class_input_framework()
def get_list_module():
    try:
        #name_module = request.args['name_module']
        frmModule = Framework()
        classModule = frmModule.get_list_of_module()
        print(classModule)
        return classModule
    except Exception as e:
        return str(e)

def get_class_module(name_module, type='module'):
    try:
        frmModule = Framework()
        nameModuleJson = frmModule.get_info_of_tool(name_module)
        #print(nameModuleJson)
        pathMain = nameModuleJson['PathMain']
        [status, classModule, classInput, classOutput] = frmModule.get_class_module(pathMain)
        if (status == False):
            raise Exception(classModule)
        if type == 'module':
            return classModule
        elif type == 'input':
            return classInput
        else:
            return classOutput
    except Exception as e:
        return e

def get_format_input(name_module):
    return get_class_module(name_module, 'input').default_format()

def run_module(data_input):
    frmFramework = Framework()
    frmFramework.Run(data_input)
    return frmFramework
