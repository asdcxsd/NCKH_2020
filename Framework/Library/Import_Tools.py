from configvalue import UPLOAD_FOLDER_TOOLS, FOLDER_TOOLS
from Framework.Library.library import  ImportTool, RemoveTool, unzip_file
def import_tool(filename):
    try:
        path = UPLOAD_FOLDER_TOOLS + filename 
        zipfile = unzip_file(path, UPLOAD_FOLDER_TOOLS)
        folder = zipfile.unzipfolder() + filename.rsplit(".", 1)[0] + "/"
        RunImport = ImportTool(folder)
        if RunImport.check_exist()>= 0 :
            print("Remove:", filename.rsplit(".", 1)[0])
            remove_tool(filename.rsplit("v", 1)[0])
        status = RunImport.update_module_file();
        if status and RunImport.have_Docker():
            RunImport.update_docker()
        if status and RunImport.have_Init():
            RunImport.copy_Init_file()
        if status:
            RunImport.copy_file()
        #status = True
    except Exception as e:
        raise e
    finally: 
        del zipfile
    return status


def remove_tool(filename):
    try:
        RunImport = RemoveTool(filename)
        
        status = RunImport.remove_module_file();
        if status and RunImport.have_Docker():
            RunImport.remove_docker()
        if status and RunImport.have_Init():
            RunImport.remove_Init_file()
        if status:
            RunImport.remove_folder_tool()
        #status = True
    except Exception as e:
        raise e
    
    return status