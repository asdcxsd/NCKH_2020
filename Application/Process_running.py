from datetime import datetime

from bson.objectid import ObjectId
from .Function.DB_Process import add_process, update_process, get_process
from Framework.Valueconfig import FORMATTIME # FORMATTIME = "%d/%m/%YT%H:%M:%S"
from Framework.Valueconfig import ValueStatus
class ProcessRunning():
    status = None
    _id = None
    date_create = None
    date_stop = None
    name = None
    target = None
    module_run = None
    def __init__(self, name, update_db = True):
        self.name = name
        self.target = "Unknow"
        dateTimeObj = datetime.now()
        self.date_create = dateTimeObj.strftime(FORMATTIME)
        self.date_stop = ""
        module_run = []
        self.status = ValueStatus.Creating
        if update_db:
            self.install_process_to_db()
        pass
    def update_module_run(self, module):
        self.module_run = module
    def change_status(self, status):
        self.status = status
        self.change_process_from_db()
        pass
    def to_json(self):
        data = {
            "Name" : self.name,
            "Target" : self.target,
            "Date_Create" : self.date_create,
            "Date_Stop" : self.date_stop,
            "Module" : self.module_run,
            "Status" : self.status
        }
        if self._id != None: 
            data["_id"] = self._id
        return data
    def update_infomation(self, name=None, target=None):
        if name != None:
            self.name = name
        if target != None:
            self.target = target
        self.update_process()

    def install_process_to_db(self):
        status, result = add_process(self.to_json())
        self._id = str(result.inserted_id)
    #return _id

    def delete_process_from_db(self):
        pass

    def change_process_from_db(self):
        data_input = {
            "_id" : ObjectId(self._id)
        }
        data_output = {
            "Status" : self.status
        }
        update_process(data_input, data_output)

    def update_process(self):
        data_input = {
            "_id" : ObjectId(self._id)
        }
        data_output = self.to_json()
        update_process(data_input, data_output)
        pass

    def update_result_process(self):
        pass

    def get_from_db(self,_id):
        self._id = _id
        input = {
            "_id" : ObjectId(_id)
        }
        status, data = get_process(input)
        data = data[0]
        self.name = data['Name']
        self.target = data['Target']
        self.status = data['Status']
        self.date_create = data['Date_Create']
        self.date_stop = data['Date_Stop']
        self.module_run = data['Module']
    def stop_run(self):
        dateTimeObj = datetime.now()
        self.date_stop = dateTimeObj.strftime(FORMATTIME)
        self.update_process()
