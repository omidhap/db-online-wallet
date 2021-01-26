from factory.database import Database


class Customer(object):
    def __init__(self):
        self.db = Database()

        self.collection_name = 'customer'

        self.fields = {
            "name": "string",
            "created": "datetime",
            "updated": "datetime",
            "wallets":[]
        }

    def create(self, customer):
        res = self.db.insert(customer, self.collection_name)
        return "Inserted Id " + res

    def find(self):
        return self.db.find(self.collection_name)

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, customer):
        return self.db.update(id, customer, self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
