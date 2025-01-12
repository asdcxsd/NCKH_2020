from .Connect_Database import use_collection

def connect_db():
    return use_collection('db_process')

def add_process(data):
    try:
        db_recon = connect_db();
        result_insert = db_recon.insert_one(data)
        return [True, result_insert]
    except Exception as e:
        return [False, str(e)]
def update_process(data_input, data_output):
    try:
        db_process=  connect_db()
        if "_id" in data_output:
            data_output.pop("_id", None)
        result_insert = db_process.find_one_and_update(data_input, {"$set" : data_output} ,upsert=True)
        return [True, result_insert]
    except Exception as e:
        return [False, str(e)]

def get_process(input):
    
    try:
        db_recon = connect_db();
        res = db_recon.find(input)
        return [True, res ]  
    except Exception as e:
        return [False, str(e)]
