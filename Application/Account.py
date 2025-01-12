
from bson.objectid import ObjectId
from Application.Function.Connect_Database import use_collection
from .Function.Connect_Framework import get_class_module
ConfigSetup = get_class_module("ConfigSetup")
def get_account(username, password):
    account_db =    use_collection('Account')
    data = {
        "username" : username,
        "password" : password
    }
    data = account_db.find(data)
  
    if (data.count() == 0):
        return False
    return data[0]


def get_account_for_update(query): 
    try: 
        account_db = use_collection("Account")
        data = account_db.find(query)
        return [True, data]
    except Exception as e: 
        return [False, str(e)]

def update_user_password(query): 
    data = {
        "_id": ObjectId(query['_id'])
    }
    account_db = use_collection("Account")
    value = account_db.find_one_and_update(data, {"$set": {"password": query['password']}})
    _id = str(value['_id'])
    return [True, _id]


def config_update_by_id(data , _id=None):
    config_setup =    use_collection('ConfigSetup')
    object_config = ConfigSetup()
    object_config.try_parse(data)
    data_json = object_config.to_json()
    [status, data] = get_config_query({"Cf_Account_id": _id})
    if _id == None or data.count() == 0 :
        insert_data = config_setup.insert_one(data_json)
        _id = str(insert_data.inserted_id)
    else:
        del data_json['Cf_Account_id']
        data = {
            "Cf_Account_id" : _id
        }
        value = config_setup.find_one_and_update(data, {
            "$set" : data_json} ,upsert=True)
        _id = str(value['_id'])
    return _id

def get_config_query(data): 
    try: 
        config = use_collection("ConfigSetup")
        result = config.find(data)
        return [True, result]
    except Exception as e: 
        return [False, str(e)]

def delete_config_with_id(data):
    try: 
        config = use_collection("ConfigSetup")
        config.remove(data)
        return True
    except Exception as e: 
        return [False, str(e)]




