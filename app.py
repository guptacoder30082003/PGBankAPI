from flask import Flask, jsonify, request
import random
import datetime
from threading import Thread
import time

app = Flask(__name__)

# Static user data (you can connect this to a database later)
users = {
    "user1": {
        "account_balance": 10000,
        "monthly_budget": 10000,
        "transactions_history": []
    }
}

# Some sample merchants for random transaction generation
merchants = ["Amazon", "Flipkart", "Swiggy", "Zomato", "Uber", "Google Play", "Paytm", "Netflix"]

# Function to generate one random transaction
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

# This will run when visiting "/" or "/transactions"
def get_transaction_data(user_id='user1'):
    if user_id not in users:
        return {"error": "User not found"}, 404

    user = users[user_id]

    now = datetime.datetime.now()
    current_month = now.month
    monthly_spent = sum(
        t["amount"] for t in user["transactions_history"]
        if t["type"] == "debit" and datetime.datetime.strptime(t["time"], "%Y-%m-%d %H:%M:%S").month == current_month
    )

    return {
        "balance": user["account_balance"],
        "transactions": user["transactions_history"][-50:],  # Latest 50
        "monthly_spent": monthly_spent,
        "monthly_budget": user["monthly_budget"]
    }

# Homepage shows transaction data
@app.route('/')
def home():
    data = get_transaction_data()
    if isinstance(data, tuple):  # error occurred
        return jsonify(data[0]), data[1]
    return jsonify(data)

# Explicit route for fetching transactions (with user_id optional)
@app.route('/transactions', methods=['GET'])
def get_transactions():
    user_id = request.args.get('user_id', 'user1')
    data = get_transaction_data(user_id)
    if isinstance(data, tuple):  # error occurred
        return jsonify(data[0]), data[1]
    return jsonify(data)

# Route to set or update monthly budget
@app.route('/set-budget', methods=['POST'])
def set_budget():
    user_id = request.json.get('user_id', 'user1')
    budget = request.json.get('monthly_budget')

    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    if not budget or budget <= 0:
        return jsonify({"error": "Invalid budget value"}), 400

    users[user_id]["monthly_budget"] = budget
    return jsonify({"message": "Budget updated successfully"}), 200

# Background task to auto-generate transactions every 10 seconds
def generate_transactions_periodically():
    while True:
        time.sleep(10)
        generate_transaction('user1')

if __name__ == '__main__':
    transaction_thread = Thread(target=generate_transactions_periodically)
    transaction_thread.daemon = True
    transaction_thread.start()

    app.run(host='0.0.0.0', port=10000)
