
import os
from api.v1.uploadfile import allowed_file
from datetime import datetime
from configvalue import  UPLOAD_FOLDER_TOOLS , ALLOWED_EXTENSIONS
from flask import Blueprint, Response, request
from api.v1.output import make_output
from bson.objectid import ObjectId
from threading import Thread
from Library.Reconnai.reconnaissance import Reconnaissance
from Library.Target.target import get_target_url
def analys_tool_reconnai(filename):
    path = UPLOAD_FOLDER_TOOLS + filename 

    