
from Database.database import delete_recon
from urllib.parse import urlparse
from bson.objectid import ObjectId
from flask import Blueprint, Response, request
from Library.Target.target import get_target, put_target, delete_target, get_target_url
from api.v1.output import make_output
Target = Blueprint('Target', __name__)
import xml.etree.ElementTree as ET

@Target.route('/gettarget', methods=['GET'])
def get_url_by_id():
    try:
        target_id = request.args['target_id']
        [status, data]  = get_target_url(target_id)
        data['_id'] = str(data["_id"])
        if status :
            return Response(make_output(data = data, message ='success'), mimetype="application/json", status=200)
        else:
            raise Exception("Target not exist!")
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)

@Target.route('/getall', methods=['GET'])
def request_get_all_target():
    try:
        [status, data] = get_target({})
        result = [{"url": i['url'], "_id": str(i['_id']), "name" : i['name']} for i in data]
        if status :
            return Response(make_output(data = result, message ='success'), mimetype="application/json", status=200)
        else:
            raise Exception(data)
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)

@Target.route('/insert', methods=['POST'])
def request_put_target():
    try:
        url = request.form['url']
        name = request.form['name']
        parsed_uri =  urlparse(url)
        url = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        [status, data] = get_target({'name': name})
        if data.count()== 0: 
            result = put_target({'url': url, 'name': name})
        else: 
            raise Exception("Name exist!")
        if status ==True :
            return Response(make_output(data = "Update success", message = str(result.inserted_id)), mimetype="application/json", status=200)
        else: 
            raise Exception("Insert Error")
    except Exception as e:
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)



@Target.route('/delete', methods=['DELETE'])
def request_delete_target():
    try:
        data_remove = {}
        if "url" in request.form: 
            url = request.form['url']
            data_remove['url'] = url
        if "target_id" in request.form: 
            target_id = request.form['target_id']
            data_remove['_id'] = ObjectId(target_id)
        [status, data] = get_target(data_remove)
        if status == False: raise Exception(data)
        if (data.count() > 0):
            status= delete_target(data_remove)
            if "_id" in data_remove:
                data_remove = {'target_id': str(data_remove['_id'])}
                status = delete_recon(data_remove)
            #delete all 

            #dedlete all --
        else: raise Exception("Target not exist!")
        return Response(make_output(data = "delete success", message ='success'), mimetype="application/json", status=200)
    except Exception as e:    
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)

