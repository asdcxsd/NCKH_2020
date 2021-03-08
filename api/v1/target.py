
from urllib.parse import urlparse
from bson.objectid import ObjectId
from flask import Blueprint, Response, request
from target import get_target, put_target, delete_target, get_target_url
from api.v1.output import make_output
Target = Blueprint('Target', __name__)
import xml.etree.ElementTree as ET

@Target.route('/geturl', methods=['POST'])
def get_url_by_id():
    target_id = request.form['target_id']
    [status, data]  = get_target_url(target_id)
    if status :
        return Response(make_output(data = data, message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= str(status) ), mimetype="application/json", status=404)

@Target.route('/getall', methods=['GET'])
def request_get_all_target():
    [status, data] = get_target({})
    result = [{"url": i['url'], "id": str(i['_id'])} for i in data]
    if status :
        return Response(make_output(data = result, message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= str(result) ), mimetype="application/json", status=404)


@Target.route('/insert', methods=['POST'])
def request_put_target():
    url = request.form['url']
    parsed_uri =  urlparse(url)
    url = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    [status, data] = get_target({'url': url})
    if (data.count() == 0):
        status= put_target({'url': url})
    else:
        status = "target exist!"

    if status ==True :
        return Response(make_output(data = "Update success", message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= str(status) ), mimetype="application/json", status=404)



@Target.route('/delete', methods=['DELETE'])
def request_delete_target():
    data_remove = {}
    if "url" in request.form: 
        url = request.form['url']
        data_remove['url'] = url
    if "target_id" in request.form: 
        target_id = request.form['target_id']
        data_remove['_id'] = ObjectId(target_id)
    [status, data] = get_target(data_remove)
    if (data.count() > 0):
        status= delete_target(data_remove)
    else:
        status = "target not exist!"

    if status ==True :
        return Response(make_output(data = "delete success", message ='success'), mimetype="application/json", status=200)
    else:
        return Response(make_output(message =  "fail", data= str(status) ), mimetype="application/json", status=404)

