from bson.objectid import ObjectId
from Database.database import connect_target

class Target:
    _id = ""
    Name = ""
    URL = ""
    def __init__(self):
        pass
    def __init__(self, id):
        [status, result] = get_target({"_id" : ObjectId(id)})
        if not status or result.count() == 0: raise Exception("Target ID not exist") 
        self._id = id
        self.Name = result[0]['name']
        self.URL = result[0]['url']
def get_target(data):
    try:
        db_target = connect_target();
        res = db_target.find(data)
        return [True, res ]  
    except Exception as e:
        return [False, str(e)]

def put_target(data):
    try:
        db_target = connect_target();
        result = db_target.insert_one(data)
        return result
    except Exception as e:
        raise e
def delete_target(data):
    try:
        db_target = connect_target();
        db_target.remove(data)
        return True
    except Exception as e:
        return str(e)

def check_exist(url):
    [status, data] = get_target({'url': url})
    if (status and data.count() > 0):
        return True
    else:
        return False

def get_target_id(url):
    [status, data] = get_target({'url': url})
    if (data.count() == 0):
        status= put_target({'url': url})
        if (status != True):
            return [False, str(status)]
        else:
            [status, data] = get_target({'url': url})
    
    return [True, str(data[0]['_id'])]


def get_target_url(target_id):
    [status, data] = get_target({'_id': ObjectId(target_id)})
    if (data.count() == 0):
        return [False, str(status)]
    
    return [True, data[0]]
