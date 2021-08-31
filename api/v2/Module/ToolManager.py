from Framework.Framework import Framework
from api.v1.output import make_output
from flask import request, Blueprint, Response
from Application.Function.Connect_Framework import get_class_module

ToolManager = Blueprint("ToolManager", __name__)

@ToolManager.route('/getall', methods=['POST'])
def get_all_tool(): 
    try: 
        print(request.form['module_name'])
        if "module_name" in request.form: 
            framework = Framework()
            List_all_tool = framework.get_list_of_module(request.form['module_name'])
            result = []
            for i in List_all_tool: 
                result.append(framework.get_info_main_module(i))
            print(result)
            return Response(make_output(data=result, message="success"), mimetype="application/json", status=200)
    except Exception as e: 
        return Response(make_output(data=str(e), message="fail"), mimetype="application/json", status=404)


        

