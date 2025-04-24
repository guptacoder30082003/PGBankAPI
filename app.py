from flask import Flask, jsonify
import random
import datetime
from threading import Thread
import time

app = Flask(__name__)

# Sample user data
users = {
    "user1": {
        "account_balance": 10000,
        "transactions_history": []
    }
}

# Sample merchants list
merchants = ["Amazon", "Flipkart", "Swiggy", "Zomato", "Uber", "Google Play", "Paytm", "Netflix"]

# Generate one transaction
def generate_transaction(user_id):
    user = users[user_id]
    merchant = random.choice(merchants)
    amount = random.randint(50, 500)
    transaction_type = "debit" if random.random() > 0.1 else "credit"
    time_of_transaction = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if transaction_type == "debit":
        user["account_balance"] -= amount
    else:
        user["account_balance"] += amount

    transaction = {
        "merchant": merchant,
        "amount": amount,
        "type": transaction_type,
        "time": time_of_transaction
    }

    user["transactions_history"].append(transaction)
    return transaction

# API to return latest transaction and balance
@app.route('/')
def home():
    user = users["user1"]
    last_transaction = user["transactions_history"][-1] if user["transactions_history"] else None

    return jsonify({
        "balance": user["account_balance"],
        "transaction": last_transaction
    })

# Background thread to auto-generate a transaction every 10 seconds
def transaction_generator():
    while True:
        time.sleep(10)
        generate_transaction("user1")

if __name__ == '__main__':
    thread = Thread(target=transaction_generator)
    thread.daemon = True
    thread.start()

    app.run(host='0.0.0.0', port=10000)
