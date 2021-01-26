from factory.database import Database


class Staff(object):
    def __init__(self):
        self.db = Database()

        self.collection_name = 'staff'

        self.fields = {
            "name": "string",
            "role": "string",
            "status": "string",
            "created": "datetime",
            "updated": "datetime",
        }

    def create(self, staff):
        res = self.db.insert(staff, self.collection_name)
        return "Inserted Id " + res

    def find(self):
        return self.db.find(self.collection_name)

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, staff):
        return self.db.update(id, staff, self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
