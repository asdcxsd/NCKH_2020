
from urllib.parse import urlparse
from bson.objectid import ObjectId
from flask import Blueprint, Response, request
from api.v1.output import make_output
from Framework.Framework import Framework
from Application.AppMain import Run
Main = Blueprint('Main', __name__)

# run all function 
@Main.route('/run', methods=['POST'])
def run_framework():
    pass

# run only target 
@Main.route('/run', methods=['POST'])
def run_framework():
    pass

