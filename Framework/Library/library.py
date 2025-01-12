from Framework.Library.Function_main import get_class_module, read_data_json_from_file, write_data_json_to_file
import os, json
from os.path import isfile, join
from posix import listdir
import shutil, zipfile
from Framework.Library.Function.manager_docker import ImagesDocker
from configvalue import UPLOAD_FOLDER_TOOLS, FOLDER_TOOLS

def mergeDict(dict1, dict2):
    try:  
        dict3 = {**dict1, **dict2}
        for key, value in dict3.items():
            if key in dict1 and key in dict2:
                    try:
                        dict3[key] = list(set(value + dict1[key]))
                    except:
                        dict3[key]  = mergeDict(value, dict1[key])
        return dict3
    except Exception as e:
        print("Error conver data", e);
        return dict1

#---
class unzip_file:
    source = ''
    destination = ''
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
    def __del__(self):
        try:
            shutil.rmtree(self.source[:-4])
        except Exception as e:
            raise e 

    def unzipfolder(self):
        #unzip file to folder session/
        try:
        
            with zipfile.ZipFile(self.source, 'r') as zip_ref:
                zip_ref.extractall(self.destination)
            return self.destination
        except Exception as e :
            raise e 

class ImportTool():
    config_tools = {}
    def __init__(self, folder):
        self.folder = folder
        try:
            with open(folder + "config-tools.json", "r") as file:
                data = file.read();
                data_json = json.loads(data)
            self.config_tools = data_json
        except Exception as e:
            print(e)
    def check_exist(self):
        data = read_data_json_from_file("Library/Module.json")
        for index, module in enumerate(data['Module']):
            if self.config_tools["NameModule"] ==  module["NameModule"] and self.config_tools["TypeModule"] ==  module["TypeModule"]:
                if (self.config_tools["Version"]  <=  module["Version"]):
                    print("Tool exist!", self.config_tools["Version"], module["Version"] )
                    return -1
                print("Tool outdate!")
                return index
        print("Tool not exist!")
        return -2
    def update_module_file(self):
        checker = self.check_exist()
        if checker == -1: 
            return
        data = read_data_json_from_file("Library/Module.json")
        module_write = self.config_tools['Module']
        module_write['NameModule'] = self.config_tools['NameModule']
        module_write['TypeModule'] = self.config_tools['TypeModule']
        module_write['Version'] = self.config_tools['Version']
        if checker == -2:
            data['Module'].append(module_write)
        else:
            data['Module'][checker] = module_write
        for key, value in   self.config_tools['ValueOutput'].items():
            if key not in data['ValueOutput'].keys():
                data['ValueOutput'][key] = value
        for key, value in   self.config_tools['ClassMergeData'].items():
            if key not in data['ClassMergeData'].keys():
                data['ClassMergeData'][key] = value
        for key, value in   self.config_tools['ValueConfig'].items():
            if key not in data['ValueConfig'].keys():
                data['ValueConfig'][key] = value
        status = write_data_json_to_file("Library/Module.json", data)
        return status
    def copy_file(self):
        folder_init = self.folder + self.config_tools['Folder'] + "/"
        destination = FOLDER_TOOLS + self.config_tools['TypeModule'].split("_")[1] + "/"
        shutil.copytree(folder_init, destination  + self.config_tools['Folder'])
    def copy_Init_file(self):
        pass
    def update_docker(self):
        try:    
            if not self.have_Docker(): return False
            Images  = ImagesDocker()
            Images.name = self.config_tools['Docker']["Name"]
            if Images.check_exist() : 
                raise Exception("Tools exist!")
            else:
                if self.config_tools['Docker']["Type"] == "File":
                    Images.add_images(self.folder + self.config_tools['Docker']["Path"] )
                if self.config_tools['Docker']["Type"] == "Pull":
                    Images.pull_images(self.config_tools['Docker']["Name"] )
        except Exception as e:
            print("Error import tool" , e)
            #raise e
        return True
    def have_Docker(self):
        return  self.config_tools["Docker"] != None
    def have_Init(self):
        return self.config_tools['Init_Folder'] != None
def copy_extension_of_tool(folderroot, destination):
    try:
        with open(folderroot + "config.json", "r") as file:
            data_string = file.read()
            file.close()
        data_json = json.loads(data_string)
        folder = folderroot + "extension/" + data_json['name_extension']
        if os.path.isfile(destination  + data_json['name_extension']):
            raise Exception("Tools exist!")
        
        shutil.copyfile(folder, destination  + data_json['name_extension'])

        if "init_folder" in data_json: 
            folder_init = folderroot + data_json['init_folder']
            shutil.copytree(folder_init, destination + "../" + "init_tools/" + data_json['init_folder'])

    except Exception as e:
        print("Error import tool" , e)
        raise e
    return True


class RemoveTool():
    config_tools = {}
    def __init__(self, module):
        self.module = module
    def check_exist(self):
        data = read_data_json_from_file("Library/Module.json")
        for index, module in enumerate(data['Module']):
            if self.module ==  module["NameModule"]:
                return index
        print("Tool not exist!")
        return -2
    def remove_module_file(self):
        checker = self.check_exist()
        if checker == -2: 
            return
        data = read_data_json_from_file("Library/Module.json")
        pathMain = data["Module"][checker]['PathMain']
        self.folder_module = FOLDER_TOOLS[:-1]+  pathMain.rsplit("/", 1)[0]
        [status, classModule, classInput, classOutput] = get_class_module(pathMain)
        if checker != -2:
            del data["Module"][checker]
        self.classModule = classModule()
        status = write_data_json_to_file("Library/Module.json", data)
        return status
    def remove_folder_tool(self):
        shutil.rmtree(self.folder_module)
    def remove_Init_file(self):
        pass
    def remove_docker(self):
        try:    
            if not self.have_Docker(): return False
            Images  = ImagesDocker()
            Images.name = self.classModule.docker_name
            if Images.check_exist() : 
                Images.remove_images()
            else:
               raise Exception("Tools not exist!")
        except Exception as e:
            print("Error remove tool" , e)
            raise e
        return True
    def have_Docker(self):
        if hasattr(self.classModule,"docker_name"):
            return self.classModule.docker_name != None
        return False
    def have_Init(self):
        if hasattr(self.classModule,"init_folder"):
            return self.classModule.init_folder != None
        return False



def delete_docker_to_computer(name_tool):
    Recon = Reconnaissance()
    result = Recon.get_all_extension()
    for fo in result:
        func = fo.reconnaissance()
        info = func.info()
        if info['name'] == name_tool:
            #print("havr Toolssssssssssssss")   
            try:
                Images  = ImagesDocker()
                Images.name =func.name
                if Images.check_exist() == False : 
                    raise Exception("Tools not exist!")
                else:
                    Images.remove_images()
            except Exception as e: 
                print(e)
                
            try:
                
                fileextension = func.filename
                os.remove(FOLDER_TOOLS  + "extension/" + fileextension)
            except Exception as e: 
                print (e)
                pass
            try:
                folder_info  = func.init_folder

                shutil.rmtree(FOLDER_TOOLS + "init_tools/" + folder_info)

            except Exception as e:
                print(e)


    return True

def get_file_of_folder(folder):
    from os import listdir
    from os.path import isfile, join
    onlyfile = [f for f in listdir(folder) if isfile(join(folder, f))]
    ans = 0
    result = []
    for i in onlyfile:
        if ".zip" in i :
            result.append(i.rsplit(".", 1)[0])
    return result 
#--