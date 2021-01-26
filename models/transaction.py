from factory.database import Database


class Transaction(object):
    def __init__(self):
        self.db = Database()

        self.collection_name = 'transaction'

        # self.fields = {
        #     "fromWallet": "string",
        #     "toWallet": "string",
        #     "amount": "string",
        #     "status": "string",
        #     "created": "datetime",
        #     "updated": "datetime",
        # }

    def create(self, transaction):
        res = self.db.insert(transaction, self.collection_name)
        return "Inserted Id " + res

    def find(self):
        return self.db.find(self.collection_name)

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, transaction):
        return self.db.update(id, transaction, self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)

    def find_by_from_to(self, fromid, toid):
        return self.db.find_by_from_to( fromid, toid, self.collection_name)

    def find_by_date(self, date):
        return self.db.find_by_date(date, self.collection_name)

    def find_by_from_or_to(self, wid):
        return self.db.find_by_from_or_to(wid, self.collection_name)
