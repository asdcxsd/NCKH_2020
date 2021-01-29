
import string
from flask import Blueprint, Response, request
from pymongo import results
from database import get_recon
from api.v1.output import make_output
from POCURI import POCURI
Poc = Blueprint('Poc', __name__)
import xml.etree.ElementTree as ET



@Poc.route('/tools', methods=['GET'])
def get_all_tools():
    CPOC = POCURI()
    result = CPOC.get_all_pocs()
    print(result)
    if not isinstance(result, str):
        return Response(make_output(data = result, message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= result ), mimetype="application/json", status=404)

