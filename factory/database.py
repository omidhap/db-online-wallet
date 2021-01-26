from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
from datetime import timedelta
from config import config


class Database(object):
    def __init__(self):
        self.client = MongoClient(config['db']['url'])
        self.db = self.client[config['db']['name']]

    def insert(self, element, collection_name):
        element["created"] = datetime.now()
        element["updated"] = datetime.now()
        inserted = self.db[collection_name].insert_one(element)
        return str(inserted.inserted_id)

    def find(self, collection_name):

        found = self.db[collection_name].find()

        found = list(found)

        for i in range(len(found)):
            if "_id" in found[i]:
                found[i]["_id"] = str(found[i]["_id"])

        return found

    def find_by_id(self, id, collection_name):
        found = self.db[collection_name].find_one({"_id": ObjectId(id)})

        if found is None:
            return "Not found!"

        if "_id" in found:
            found["_id"] = str(found["_id"])

        return found

    def update(self, id, element, collection_name):
        criteria = {"_id": ObjectId(id)}

        element["updated"] = datetime.now()
        set_obj = {"$set": element}

        updated = self.db[collection_name].update_one(criteria, set_obj)
        if updated.matched_count == 1:
            return "Record Successfully Updated"

    def delete(self, id, collection_name):
        deleted = self.db[collection_name].delete_one({"_id": ObjectId(id)})
        return bool(deleted.deleted_count)

    def find_by_id_name(self, id, name, collection_name):
        found = self.db[collection_name].find_one({"_id": ObjectId(id), "name": name})

        if found is None:
            return "Not found!"

        if "_id" in found:
            found["_id"] = str(found["_id"])

        return found

    def find_by_from_to(self, fromid, toid, collection_name):
        found = self.db[collection_name].find({"fromWallet": fromid, "toWallet": toid})
        found = list(found)

        for i in range(len(found)):
            if "_id" in found[i]:
                found[i]["_id"] = str(found[i]["_id"])

        return found


    def find_by_from_or_to(self, wid, collection_name):
        found = self.db[collection_name].find({"fromWallet": wid})
        found2 =self.db[collection_name].find({"toWallet": wid})

        found = list(found)
        found2 = list(found2)

        for i in range(len(found2)):
            found.append(found2[i])
        found3 = list(found)

        for i in range(len(found3)):
            if "_id" in found3[i]:
                found3[i]["_id"] = str(found3[i]["_id"])

        return found3


    def find_by_customer_id(self, cid, collection_name):
        found = self.db[collection_name].find({"customerID": cid})
        found = list(found)

        for i in range(len(found)):
            if "_id" in found[i]:
                found[i]["_id"] = str(found[i]["_id"])

        return found


    def find_by_date(self, date, collection_name):
        found = self.db[collection_name].find({"created": date})
        found = list(found)
        self.db[collection_name].find({"created": {"$eq": datetime.now() - timedelta(int(date))}})
        for i in range(len(found)):
            if "_id" in found[i]:
                found[i]["_id"] = str(found[i]["_id"])

        return found
