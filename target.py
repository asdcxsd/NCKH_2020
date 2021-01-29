from bson.objectid import ObjectId
from database import target, connect


def get_target(data):
    try:
        db_target = target();
        res = db_target.find(data)
        return [True, res ]  
    except Exception as e:
        return [False, str(e)]

def put_target(data):
    try:
        db_target = target();
        db_target.insert_one(data)
        return True
    except Exception as e:
        return str(e)
def delete_target(data):
    try:
        db_target = target();
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
    
    return [True, str(data[0]['url'])]
