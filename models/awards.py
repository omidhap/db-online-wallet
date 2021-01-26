from factory.database import Database


class Awards(object):
    def __init__(self):
        self.db = Database()

        self.collection_name = 'awards'

        self.fields = {
            "beginDate": "string",
            "endDate": "string",
            "condition": "string",
            "amount": "string",
            "type": "string",
            "created": "datetime",
            "updated": "datetime",
        }

    def create(self, awards):
        res = self.db.insert(awards, self.collection_name)
        return "Inserted Id " + res

    def find(self):
        return self.db.find(self.collection_name)

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, awards):
        return self.db.update(id, awards, self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
