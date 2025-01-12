#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson.objectid import ObjectId
from pymongo import MongoClient
import json
from bson.json_util import dumps
import datetime
from configvalue import *
global DB
def connect():
    try:
        global DB
        client = MongoClient(host=MONGODB_HOST, port=MONGODB_PORT, username = MONGODB_USERNAME, password= MONGODB_PASSWORD)
        DB = client[MONGODB_NAMEDB]
        print("[+] Connect database ok", datetime.datetime.now())
    except Exception as ex:
        print("[-] Open faill database")
        print("\tError ", ex)
        return 0
def use_collection(name_collection):
    try:
        db_recon = DB[name_collection]
    except Exception as e:
        print(str(e))
        connect()
        db_recon = DB[name_collection]
    return db_recon  

def connect_account(): 
    return use_collection("Account"); 

def connect_target():
    return use_collection('Target')

def get_ip_record(data): 
    try: 
        db_input = use_collection("Module_Input")
        result = json.loads(dumps(db_input.find({"_id":ObjectId(data)})))[0]
        ip = result['IN_IP']
        return [True, ip]
    except Exception as e: 
        return [False, str(e)]

# def update_recon(datainput, datanew):
#     try:
#         db_recon = reconnaissance();
#         result_insert = db_recon.find_one_and_update(datainput, {
#             "$set" : datanew} ,upsert=True)
#         return [True, result_insert]
#     except Exception as e:
#         return [False, str(e)]

def get_input(data): 
    try: 
        db_module_input = use_collection("Module_Input")
        Module_input_id = db_module_input.find(data)
        return [True, Module_input_id]
    except Exception as e: 
        return [False, str(e)]
    
def get_all_input(): 
    try: 
        db_module_input = use_collection("Module_Input")
        result = db_module_input.find({})
        return [True, result]
    except Exception as e: 
        return [False, str(e)]    

def get_all_process(): 
    try: 
        db_process = use_collection("db_process")
        result = db_process.find({})
        return [True, result]
    except Exception as e: 
        return [False, str(e)]


def get_process_with_query(query): 
    try: 
        db_process = use_collection("db_process")
        result = db_process.find(query)
        return [True, result]
    except Exception as e: 
        return [False, str(e)]


        


def remove_input(data): 
    try: 
        db_module_input = use_collection("Module_Input")
        db_module_input.remove(data)
        return True
    except Exception as e: 
        return False
        
def reconnaissance():
    return use_collection('Module_Reconnaissance')


def put_recon(data):
    try:
        db_recon = reconnaissance();
        result_insert = db_recon.insert_one(data)
        return [True, result_insert]
    except Exception as e:
        return [False, str(e)]
def get_recon(data):
    try:
        db_recon = reconnaissance();
        res = db_recon.find(data)
        return [True, res ]  
    except Exception as e:
        return [False, str(e)]

def delete_recon(data):
    try:
        db_recon = reconnaissance();
        db_recon.remove(data)
        return True
    except Exception as e:
        return str(e)  
          
def exploit_cve():
    return use_collection('Module_Exploit')

def put_exploit_cve(data):
    try:
        db_cve = exploit_cve()
        db_cve.insert_one(data)
        return True
    except Exception as e:
        return str(e)

def delete_exploit_cve(data): 
    try: 
        db_cve = exploit_cve(); 
        db_cve.remove(data)
        return True
    except Exception as e: 
        return str(e) 

def get_exploit_cve(data):
    try:
        db_recon = exploit_cve();
        res = db_recon.find(data)
        return [True, res ]  
    except Exception as e:
        return [False, str(e)]


def get_pocs_with_id(target_id):
    [status, data] = get_exploit_cve({'_id': ObjectId(target_id)})
    if (data.count() == 0):
        return [False, str(status)]
    return [True, data[0]]

def get_shell_log_data(data): 
    try: 
        db_shell = use_collection("Module_Output")
        res = db_shell.find(data)
        return [True, res]
    except Exception as e: 
        return [False, str(e)]


def save_result_to_db(data_json, data_process, data_input):
    data_json = data_json['Result']
    data_input = data_input['Input']
    for key in data_json.keys():
        name_db = key
        data = data_json[key]
        data['_id_process'] = data_process['_id']
        data['pre_type_module'] = data_input
        db_connect = use_collection(key)
        result_insert = db_connect.insert_one(data)
        #update input_data
        data_input = [{
            'module' : key,
            '_id' : str(result_insert.inserted_id)
        }]

def get_data_from_db(name_db, _id):
    db_collections = use_collection(name_db);
    data = db_collections.find({'_id': ObjectId(_id)})
    if (data.count() == 0):
        return [False, str("Error")]
    return [True, data[0]]
def get_data_from_db_with_process(name_db, _id):
    db_collections = use_collection(name_db);
    data = db_collections.find({'_id_process': _id})
    if (data.count() == 0):
        return [False, str("Error")]
    return [True, data[0]]

def remove_data_from_db(name_db, _id, field_remove='_id'):
    db_collections = use_collection(name_db);
    if field_remove=='_id':
        _id = ObjectId(_id)
    data = db_collections.remove({field_remove: _id})
    if (data['n'] == 0):
        return [False, str("Error")]
    return [True, data]

def find_data_from_db(name_db, data): 
    try: 
        db_module_input = use_collection(name_db)
        data = db_module_input.find(data)
        if (data.count() == 0):
            return [False, str("Error")]
        return [True, data]
    except Exception as e: 
        return [False, str(e)]    
if __name__ == "__main__":
    connect();