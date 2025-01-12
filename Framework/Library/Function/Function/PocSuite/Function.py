import json
def decode_data_input_poc(data_input):
    data_input = json.loads(data_input)
    header = data_input['Referer']
    input =   data_input['Input']
    return input, header

def encode_data_input_poc(data_input, Referer=''):
    data = {
        "Referer" : Referer,
        "Input": data_input
    }
    return json.dumps(data)