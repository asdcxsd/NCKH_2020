#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson.objectid import ObjectId
from pymongo import MongoClient
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

def connect_target():
    return use_collection('Target')


def reconnaissance():
    return use_collection('reconnaissance')

def put_recon(data):
    try:
        db_recon = reconnaissance();
        result_insert = db_recon.insert_one(data)
        return [True, result_insert]
    except Exception as e:
        return [False, str(e)]
def update_recon(datainput, datanew):
    try:
        db_recon = reconnaissance();
        result_insert = db_recon.find_one_and_update(datainput, {
            "$set" : datanew} ,upsert=True)
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
    return use_collection('exploitcve')
def put_exploit_cve(data):
    try:
        db_cve = exploit_cve()
        db_cve.insert_one(data)
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

if __name__ == "__main__":
    connect();