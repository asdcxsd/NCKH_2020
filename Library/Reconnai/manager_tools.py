
from Library.Reconnai.function_recon import copy_extension_of_tool, delete_docker_to_computer, get_file_of_folder, import_docker_to_computer, unzip_file
import os
from api.v1.uploadfile import allowed_file
from datetime import datetime
from configvalue import  UPLOAD_FOLDER_TOOLS , FOLDER_TOOLS
from flask import Blueprint, Response, request
from api.v1.output import make_output
from bson.objectid import ObjectId
from threading import Thread
from Library.Reconnai.reconnaissance import Reconnaissance
from Library.Target.target import get_target_url
def import_tool_reconnai(filename):
    try:
        path = UPLOAD_FOLDER_TOOLS + filename 
        zipfile = unzip_file(path + ".zip", UPLOAD_FOLDER_TOOLS)
        folder = zipfile.unzipfolder()
        status = copy_extension_of_tool(path + "/", FOLDER_TOOLS + "extension/")
        if status: 
            status = import_docker_to_computer(path + "/")
    except Exception as e:
        raise e
    finally: 
        del zipfile
    return status


def remove_tool_reconnai(filename):
    try:
        status = delete_docker_to_computer(filename)
    except Exception as e:
        raise e

    return status


def load_tool_import():
    try:
        path = UPLOAD_FOLDER_TOOLS 
        return get_file_of_folder(path)
    except Exception as e:
        raise e