from configvalue import FOLDER_POCS, UPDATE_FOLDER_POCS, ALLOWED_EXTENSIONS, UPLOAD_FOLDER_TOOLS
from Framework.Framework import Framework
from Application.Function.Connect_Framework import get_class_module
from flask import Blueprint, Response, request
from api.v1.output import make_output
import os

POCManager = Blueprint("POCManager", __name__)
@POCManager.route("/getall", methods=['GET'])
def get_all_poc(): 
    try: 
        ClassPOCCheck = get_class_module("PocCheck", "module")
        objectPOCCheck = ClassPOCCheck()
        listPOC = objectPOCCheck.get_all_pocs()
        list_detail_POC = []
        for i in listPOC: 
            temp = objectPOCCheck.get_info_pocs(i)
            poc_detail = {}
            poc_detail['appVersion'] = temp["appVersion"]
            poc_detail['appName'] = temp['appName']
            poc_detail['createDate'] = temp['createDate']
            poc_detail['desc'] = temp['desc']
            list_detail_POC.append(poc_detail)
        return Response(make_output(data=list_detail_POC, message="success"), mimetype="application/json", status=200)
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)
    


@POCManager.route("/pocdashboard", methods=['GET'])
def get_poc_dashboard(): 
    try: 
        ClassPOCCheck = get_class_module("PocCheck", "module")
        objectPOCCheck = ClassPOCCheck()
        listPOC = objectPOCCheck.get_all_pocs()
        list_POC_type = {}
        for i in listPOC: 
            temp = objectPOCCheck.get_info_pocs(i)
            pocType = temp['appPowerLink']["pocType"]
            if pocType not in list_POC_type: 
                list_POC_type[pocType] = 1
            else: 
                list_POC_type[pocType] += 1
        print(list_POC_type)
        return Response(make_output(data=list_POC_type, message="success"), mimetype="application/json", status=200)
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)



@POCManager.route('/getdetail', methods=['POST'])
def get_detail_poc(): 
    try : 
        if "poc_name" in request.form: 
            poc_name = request.form['poc_name']
            ClassPOCCheck = get_class_module("PocCheck", "module")
            objectPOCCheck = ClassPOCCheck()
            result = objectPOCCheck.get_info_pocs(poc_name)
            return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
        else: 
            raise Exception('invalid poc name')
    except Exception as e : 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@POCManager.route('/import', methods=['PUT'])
def import_poc(): 
    try : 
        if "filename" in request.form: 
            folder = UPDATE_FOLDER_POCS
            poc_name = request.form['filename']
            ClassPOCCheck = get_class_module("PocCheck", "module")
            objectPOCCheck = ClassPOCCheck()
            result = objectPOCCheck.import_pocs(folder + poc_name)
            return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
        else: 
            raise Exception('invalid filename')
    except Exception as e : 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)


@POCManager.route("/uploadpoc", methods=['POST'])
def upload_poc_request(): 
    try: 
        file=request.files['file']
        print(file.filename)
        if file and allowed_file(file.filename): 
            folder =  UPDATE_FOLDER_POCS
            file.save(os.path.join(UPDATE_FOLDER_POCS, file.filename))
            poc_name = file.filename
            ClassPOCCheck = get_class_module("PocCheck", "module")
            objectPOCCheck = ClassPOCCheck()
            result = objectPOCCheck.import_pocs(folder + "/"+poc_name)
            return Response(make_output(message =  "success", data= result), mimetype="application/json", status=200)
        else: 
            return Response(make_output(message =  "fail", data= "Allowed file types are html zip"), mimetype="application/json", status=404)
    except Exception as e: 
        print(e)
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)


@POCManager.route('/remove', methods=['DELETE'])
def remove_poc(): 
    try : 
        if "filename" in request.form: 
            poc_name = request.form['filename']
            ClassPOCCheck = get_class_module("PocCheck", "module")
            objectPOCCheck = ClassPOCCheck()
            result = objectPOCCheck.remove_pocs(poc_name)
            return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
        else: 
            raise Exception('invalid filename')
    except Exception as e : 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)