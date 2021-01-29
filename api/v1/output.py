import json
import xmltodict
format_output = {
    "data": "",
    "message": "Error"
}
def make_output(data = "", message ='Success!!'):
    try:
        output = format_output
        output['data']= data
        output['message'] = message  
        return json.dumps(output)
    except Exception as e:
        output = format_output 
        output['data']= str(e)
        output['message'] = "Error convert to json"
    
    return json.dumps(output)