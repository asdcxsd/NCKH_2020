from configvalue import UPLOAD_FOLDER_TOOLS, FOLDER_TOOLS
from Framework.Library.library import  ImportTool, unzip_file
def import_tool(filename):
    try:
        path = UPLOAD_FOLDER_TOOLS + filename 
        zipfile = unzip_file(path, UPLOAD_FOLDER_TOOLS)
        folder = zipfile.unzipfolder() + filename.rsplit(".", 1)[0] + "/"
        RunImport = ImportTool(folder)
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
        path = UPLOAD_FOLDER_TOOLS + filename 
        zipfile = unzip_file(path, UPLOAD_FOLDER_TOOLS)
        folder = zipfile.unzipfolder() + filename.rsplit(".", 1)[0] + "/"
        RunImport = ImportTool(folder)
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