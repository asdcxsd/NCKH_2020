from Framework.Framework import Framework
from Application.Function.Connect_Framework import get_class_module
from flask import Blueprint, Response, request
from api.v1.output import make_output

POCManager = Blueprint("POCManager", __name__)
@POCManager.route("/getall", methods=['GET'])
def get_all_poc(): 
    try: 
        ClassPOCCheck = get_class_module("PocCheck", "module")
        objectPOCCheck = ClassPOCCheck()
        listPOC = objectPOCCheck.get_all_pocs()
        infoPOC = []
        for i in listPOC: 
            infoPOC.append(objectPOCCheck.get_info_pocs(i))
        return Response(make_output(data=infoPOC, message="success"), mimetype="application/json", status=200)
    
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)
    