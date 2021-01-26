from factory.database import Database


class Access(object):
    def __init__(self):
        self.db = Database()

        self.collection_name = 'access'

        self.fields = {
            "role": "string",
            "ability": "string",
            "type": "string",
            "amount": "string",
            "status": "string",
            "created": "datetime",
            "updated": "datetime",
        }

    def create(self, access):
        res = self.db.insert(access, self.collection_name)
        return "Inserted Id " + res

    def find(self):
        return self.db.find(self.collection_name)

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, access):
        return self.db.update(id, access, self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
