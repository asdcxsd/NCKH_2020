
import json
from urllib.parse import urlparse
from bson.objectid import ObjectId
from flask import Blueprint, Response, request
from api.v1.output import make_output
from Framework.Framework import Framework
from Application.Input.run import Run 
RunInput = Blueprint('RunInput', __name__)



# run only target 
@RunInput.route('/run', methods=['POST'])
def run_framework():
    '''
        {
            "Input":[
                {
                    "module": "Target",
                    "_id" : "...."
                },
                {
                    "module": "Report",
                    "_id" : "...."
                }
            ]
        }
    '''

    try:
        if "input_raw_id" in request.form: 
           input_raw_id = request.form['input_raw_id']
           input_json_id = json.loads(input_raw_id)
           def thread_run(input_json_id):
               
           status, frmFramework = Run(input_json_id)
           
        else: raise Exception("Target not exist!")
        return Response(make_output(data = "success", message ='running'), mimetype="application/json", status=200)
    except Exception as e:    
        return Response(make_output(message =  "fail", data= str(e) ), mimetype="application/json", status=404)



@RunInput.route('/status', methods=['GET'])
def run_sframework():
    
    pass
