from Library.Reconnai.reconnaissance import Reconnaissance
import os, json
from os.path import isfile, join
from posix import listdir
import shutil, zipfile
from Library.manager_docker import ImagesDocker
from configvalue import UPLOAD_FOLDER_TOOLS, FOLDER_TOOLS
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


def copy_extension_of_tool(folder, destination):
    try:
        with open(folder + "config.json", "r") as file:
            data_string = file.read()
            file.close()
        data_json = json.loads(data_string)
        folder = folder + "extension/" + data_json['name_extension']
        if os.path.isfile(destination  + data_json['name_extension']):
            raise Exception("Tools exist!")

        shutil.copyfile(folder, destination  + data_json['name_extension'])
    except Exception as e:
        print("Error import tool" , e)
        raise e
    return True

def import_docker_to_computer(folder):
    try:
        with open(folder + "config.json", "r") as file:
            data_string = file.read()
            file.close()
        data_json = json.loads(data_string)        
        Images  = ImagesDocker()
        Images.name = data_json['RepoTags']
        if Images.check_exist() : 
            raise Exception("Tools exist!")
        else:
            Images.add_images(folder + "docker/" + data_json['path_docker'])
    except Exception as e:
        print("Error import tool" , e)
        raise e
    return True

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