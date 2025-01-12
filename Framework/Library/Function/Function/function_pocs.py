from configvalue import FOLDER_POCS
import zipfile, shutil, json, os

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


def copy_pocs(folder, destination):
    try:
        with open(folder + "config.json", "r") as file:
            data_string = file.read()
            file.close()
        data_json = json.loads(data_string)
        if os.path.isfile(destination  + "pocs/" + data_json['pocs']):
            raise Exception("Tools exist!")

        shutil.copyfile(folder  +"pocs/" + data_json['pocs'], destination  + "pocs/" + data_json['pocs'] )
        shutil.copytree(folder + "init_pocs/" + data_json['folder_init'] , destination + "init_pocs/" + data_json['folder_init'] )
    except Exception as e:
        print("Error import tool" , e)
        raise e
    return True


def delete_poc(data_poc):

    try:
        name_file = data_poc['appName'] + '.py'
        folder_init = data_poc['appPowerLink']['folder_init']
        name_file = FOLDER_POCS + "pocs/" + name_file
        folder_init = FOLDER_POCS + "init_pocs/" + folder_init
        try:
            os.remove(name_file)
        except Exception as e:
            print("Error remove poc", e)
        try:
            shutil.rmtree(folder_init)
        except Exception as e:
            print("Error remove poc", e)
        return True
    except Exception as e: 
        print (e)
        return False

