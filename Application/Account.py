
from bson.objectid import ObjectId
from Application.Function.Connect_Database import use_collection, get_data_from_db
from .Function.Connect_Framework import get_class_module
ConfigSetup = get_class_module("ConfigSetup")
def get_id_account(username, password):
    account_db =    use_collection('Account')
    data = {
        "username" : username,
        "password" : password
    }
    data = account_db.find(data)
  
    if (data.count() == 0):
        return False
    return str(data[0]['_id'])

def config_update_by_id(data , _id):
    config_setup = use_collection('ConfigSetup')
    object_config = ConfigSetup()
    object_config.try_parse(data)
    data_json = object_config.to_json()
    _id_exists = config_setup.find({"_id": _id})
    if _id_exists.count() == 0: 
        data_json['_id'] = ObjectId(_id)
        print(data_json)
        insert_data = config_setup.insert_one(data_json)
        _id = str(insert_data.inserted_id)
    else: 
        data = {
            "_id" : ObjectId(_id)
        }
        config_setup.update(data, {
            "$set" : data_json} ,upsert=True)
    return _id

