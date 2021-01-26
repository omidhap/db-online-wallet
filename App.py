from datetime import datetime
from flask import Flask, request, jsonify,session
from models import staff, customer, awards, access, transaction, wallet
from datetime import timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
app.secret_key = SECRET_KEY
staff = staff.Staff()
customer = customer.Customer()
wallet = wallet.Wallet()
awards = awards.Awards()
access = access.Access()
transaction = transaction.Transaction()


db_role="normal"

@app.route('/staff/', methods=['GET'])
def get_staffs():
    return jsonify(staff.find()), 200


@app.route('/staff/<string:staff_id>/', methods=['GET'])
def get_staff(staff_id):
    return staff.find_by_id(staff_id), 200


@app.route('/staff/', methods=['POST'])
def add_staff():
    if request.method == "POST":
        name = request.json['name']
        role = request.json['role']
        status = request.json['status']
        response = staff.create({'name': name, 'role': role, 'status': status})
        return response, 201


@app.route('/staff/<string:staff_id>/', methods=['PUT'])
def update_staff(staff_id):
    if request.method == "PUT":
        name = request.json['name']
        role = request.json['role']
        status = request.json['status']
        response = staff.update(staff_id, {'name': name, 'role': role, 'status': status})
        return response, 201


@app.route('/staff/<string:staff_id>/', methods=['DELETE'])
def delete_staff(staff_id):
    if request.method == "DELETE":
        staff.delete(staff_id)
        return "Record Deleted"


@app.route('/customer/', methods=['GET'])
def get_customers():
    return jsonify(customer.find()), 200


@app.route('/customer/<string:customer_id>/', methods=['GET'])
def get_customer(customer_id):
    return customer.find_by_id(customer_id), 200


@app.route('/customer/', methods=['POST'])
def add_customer():
    if request.method == "POST":
        name = request.json['name']
        response = customer.create({'name': name})
        return response, 201


@app.route('/customer/<string:customer_id>/', methods=['PUT'])
def update_customer(customer_id):
    if request.method == "PUT":
        name = request.json['name']
        response = customer.update(customer_id, {'name': name})
        return response, 201


@app.route('/customer/<string:customer_id>/', methods=['DELETE'])
def delete_customer(customer_id):
    if request.method == "DELETE":
        customer.delete(customer_id)
        # wallet.delete({customer_id:customer_id})

        # delete all wallet of customer
        return "Record Deleted"


@app.route('/wallet/', methods=['GET'])
def get_wallets():
    return jsonify(wallet.find()), 200


@app.route('/wallet/<string:wallet_id>/', methods=['GET'])
def get_wallet(wallet_id):
    return wallet.find_by_id(wallet_id), 200


@app.route('/wallet/', methods=['POST'])
def add_wallet():
    if request.method == "POST":
        customerID = request.json['customerID']
        VIP = request.json['VIP']
        balance = 0
        status = request.json['status']
        response = wallet.create({'customerID': customerID, 'VIP': VIP, 'status': status, 'balance': balance})
        return response, 201


@app.route('/wallet/<string:wallet_id>/', methods=['PUT'])
def update_wallet(wallet_id):
    if request.method == "PUT":
        customerID = request.json['customerID']
        VIP = request.json['VIP']
        balance = request.json['balance']
        status = request.json['status']
        response = wallet.update(wallet_id,
                                 {'customerID': customerID, 'VIP': VIP, 'status': status, 'balance': balance})
        return response, 201


@app.route('/wallet/charge/<string:wallet_id>/', methods=['PUT'])
def charge_wallet(wallet_id):
    if request.method == "PUT":
        # customerID = request.json['customerID']
        # VIP = request.json['VIP']
        charge = request.json['charge']
        balance = int(wallet.find_by_id(wallet_id)['balance']) + int(charge)
        # add transfer to table
        response = wallet.update(wallet_id, {'balance': balance})
        return response, 201


@app.route('/wallet/withdraw/<string:wallet_id>/', methods=['PUT'])
def withdraw(wallet_id):
    if request.method == "PUT":
        # customerID = request.json['customerID']
        # VIP = request.json['VIP']
        amount = request.json['amount']
        if (int(wallet.find_by_id(wallet_id)['balance']) > int(amount)):
            balance = int(wallet.find_by_id(wallet_id)['balance']) - int(amount)
            response = wallet.update(wallet_id, {'balance': balance})
            return response, 201
        else:
            response = "not available"
            return response, 201
        # add transfer to table


@app.route('/wallet/transaction/', methods=['POST'])
def transaction_():
    if request.method == "POST":
        fromWallet = request.json['from']
        toWallet = request.json['to']
        amount = request.json['amount']
        fromBalance = int(wallet.find_by_id(fromWallet)['balance'])
        toBalance = int(wallet.find_by_id(toWallet)['balance'])
        amountVal = int(amount)

        # get award


        if(fromBalance >=amountVal):
            fromBalance -=amountVal
            toBalance +=amountVal
            wallet.update(fromWallet, {'balance': fromBalance})
            wallet.update(toWallet, {'balance': toBalance})
            transaction.create({'fromWallet': fromWallet, 'toWallet': toWallet, 'amount': amount, 'status': "done"})
            response = "transaction is completed"
        else:
            response = "not enough money"
            transaction.create(
                {'fromWallet': fromWallet, 'toWallet': toWallet, 'amount': amount, 'status': "failed"})

        return response
    # add transfer to table


@app.route('/wallet/<string:wallet_id>/', methods=['DELETE'])
def delete_wallet(wallet_id):
    if 'role' in session:

        if request.method == "DELETE":
            wallet.delete(wallet_id)
            return "Record Deleted"
    else :
        return "first login"


@app.route('/awards/', methods=['GET'])
def get_all_awards():
    return jsonify(awards.find()), 200


@app.route('/awards/<string:awards_id>/', methods=['GET'])
def get_awards(awards_id):
    return awards.find_by_id(awards_id), 200


@app.route('/awards/', methods=['POST'])
def add_awards():
    if request.method == "POST":
        type = request.json['type']
        amount = request.json['amount']
        beginDate = request.json['beginDate']
        endDate = request.json['endDate']
        condition = request.json['condition']
        response = awards.create(
            {'type': type, 'amount': amount, 'beginDate': beginDate, 'endDate': endDate, 'condition': condition})
        return response, 201


@app.route('/awards/<string:awards_id>/', methods=['PUT'])
def update_awards(awards_id):
    if request.method == "PUT":
        type = request.json['type']
        amount = request.json['amount']
        beginDate = request.json['beginDate']
        endDate = request.json['endDate']
        condition = request.json['condition']
        response = awards.update(awards_id, {'type': type, 'amount': amount, 'beginDate': beginDate, 'endDate': endDate,
                                             'condition': condition})
        return response, 201


@app.route('/awards/<string:awards_id>/', methods=['DELETE'])
def delete_awards(awards_id):
    if request.method == "DELETE":
        awards.delete(awards_id)
        return "Record Deleted"


@app.route('/access/', methods=['GET'])
def get_accesses():
    return jsonify(access.find()), 200


@app.route('/access/<string:access_id>/', methods=['GET'])
def get_access(access_id):
    return access.find_by_id(access_id), 200


@app.route('/access/', methods=['POST'])
def add_access():
    if request.method == "POST":
        ability = request.json['ability']
        role = request.json['role']
        status = request.json['status']
        amount = request.json['amount']
        type = request.json['type']
        response = access.create({'ability': ability, 'role': role, 'status': status, 'amount': amount, 'type': type})
        return response, 201


@app.route('/access/<string:access_id>/', methods=['PUT'])
def update_access(access_id):
    if request.method == "PUT":
        ability = request.json['ability']
        role = request.json['role']
        status = request.json['status']
        amount = request.json['amount']
        type = request.json['type']
        response = access.update(access_id,
                                 {'ability': ability, 'role': role, 'status': status, 'amount': amount, 'type': type})
        return response, 201


@app.route('/access/<string:access_id>/', methods=['DELETE'])
def delete_access(access_id):
    if request.method == "DELETE":
        access.delete(access_id)
        return "Record Deleted"


@app.route('/transaction/', methods=['GET'])
def get_transactions():
    return jsonify(transaction.find()), 200


@app.route('/transaction/<string:transaction_id>/', methods=['GET'])
def get_transaction(transaction_id):
    return transaction.find_by_id(transaction_id), 200


@app.route('/transaction/', methods=['POST'])
def add_transaction():
    if request.method == "POST":
        fromWallet = request.json['fromWallet']
        toWallet = request.json['toWallet']
        amount = request.json['amount']
        status = request.json['status']
        # transaction.create()
        response = transaction.create({'fromWallet': fromWallet, 'toWallet': toWallet, 'amount': amount, 'status': status})
        return response, 201


@app.route('/transaction/<string:transaction_id>/', methods=['PUT'])
def update_transaction(transaction_id):
    if request.method == "PUT":
        fromWallet = request.json['fromWallet']
        toWallet = request.json['toWallet']
        amount = request.json['amount']
        status = request.json['status']
        response = transaction.update(transaction_id, {'fromWallet': fromWallet, 'toWallet': toWallet, 'amount': amount,'status': status})
        return response, 201


@app.route('/transaction/<string:transaction_id>/', methods=['DELETE'])
def delete_transaction(transaction_id):
    if request.method == "DELETE":
        transaction.delete(transaction_id)
        return "Record Deleted"


@app.route('/login/', methods=['post'])
def login():
    name = request.json['name']
    password = request.json['password']
    session['role'] = staff.find_by_id_name(password , name)['role']
    session['username'] = name
    return session['role']



@app.route('/query1', methods=['post'])
def query1():
    if('role' in session):
        if(session['role']=="admin"):
            fromWal = request.json['fromWal']
            toWal = request.json['toWal']
            return jsonify(transaction.find_by_from_to(fromWal,toWal))
        else:
            return ("warning!! your role is :"+session['role'])
    else:
        return("not permitted")







@app.route('/query2', methods=['post'])
def query2():
    if ('role' in session):
        if (session['role'] == "admin"):
            walletId = request.json['walId']
            return  str((datetime.now() - wallet.find_by_id(walletId)['created']).total_seconds() / 3600) + "  hours"
        else:
            return ("warning!! your role is :" + session['role'])

    else:
        return ("not permitted")






@app.route('/query3', methods=['post'])
def query3():
    if ('role' in session):
        if (session['role'] == "admin"):
            customerId = request.json['cusId']
            return  jsonify(wallet.find_by_customer_id(customerId))
        else:
            return ("warning!! your role is :" + session['role'])
    else:
        return ("not permitted")




@app.route('/query4', methods=['post'])
def query4():
    if ('role' in session):
        if (session['role'] == "staff"):
            transactionID = request.json['tid']
            return  jsonify(transaction.find_by_id(transactionID))

        else:
                return ("warning!! your role is :"+session['role'])
    else:
        return("not permitted")


@app.route('/query5', methods=['post'])
def query5():
    if ('role' in session):
        if (session['role'] == "guest"):
            walId = request.json['wid']
            return "your balance:   "+str(wallet.find_by_id(walId)['balance'])



@app.route('/query6', methods=['post'])
def query6():
    if ('role' in session):
        if (session['role'] == "admin"):
            walId = request.json['wid']
            return jsonify(transaction.find_by_from_or_to(walId))
        else:
            return ("warning!! your role is :" + session['role'])
    else:
        return ("not permitted")
@app.route('/query7', methods=['post'])
def query7():
    if ('role' in session):
        if (session['role'] == "customer"):
            date = request.json['date']
            return  jsonify(transaction.find_by_date(date))
        else:
            return ("warning!! your role is :" + session['role'])
    else:
        return ("not permitted")

if __name__ == '__main__':
    app.run(debug=True)




# procedures
# setWage

# transfer

# setAward


# Triggers

# charge

# withdraw

# wage

