import os, json
from os.path import isfile, join
from posix import listdir
import shutil, zipfile
from Library.manager_docker import ImagesDocker
class unzip_file:
    source = ''
    destination = ''
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
    def __del__(self):
        try:
            shutil.rmtree(self.destination)
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
        with open("config.json", "r") as file:
            data_string = file.read()
            file.close()
        data_json = json.loads(data_string)
        folder = folder + "extension/" + data_json['name_extesion']
        shutil.copyfile(folder, destination  + data_json['name_extesion'])
    except Exception as e:
        print("Error import tool" , e)
        return e
    return True

def import_docker_to_computer(folder):
    try:
        with open("config.json", "r") as file:
            data_string = file.read()
            file.close()
        data_json = json.loads(data_string)
        Images  = ImagesDocker(data_json['RepoTags'])
        if Images.check_exist()
        folder = folder + "extension/" + data_json['name_extesion']
    except Exception as e:
        print("Error import tool" , e)
        return e
    return True