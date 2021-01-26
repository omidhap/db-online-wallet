from factory.database import Database


class Wallet(object):
    def __init__(self):
        self.db = Database()

        self.collection_name = 'wallet'

        self.fields = {
            "customerID": "string",
            "VIP": "string",
            "balance": "string",
            "status": "string",
            "created": "datetime",
            "updated": "datetime",
        }

    def create(self, wallet):
        res = self.db.insert(wallet, self.collection_name)
        return "Inserted Id " + res

    def find(self):
        return self.db.find(self.collection_name)

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, wallet):
        return self.db.update(id, wallet, self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)

    def find_by_customer_id(self, id):
        return self.db.find_by_customer_id(id, self.collection_name)
