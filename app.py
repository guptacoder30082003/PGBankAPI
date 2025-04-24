from flask import Flask, jsonify, request
import random
import datetime
from threading import Thread
import time

app = Flask(__name__)

# Static user data for example (you can integrate with a database in real-world apps)
users = {
    "user1": {
        "account_balance": 10000,
        "monthly_budget": 10000,
        "transactions_history": []
    }
}

# List of merchants for generating random transactions
merchants = ["Amazon", "Flipkart", "Swiggy", "Zomato", "Uber", "Google Play", "Paytm", "Netflix"]

# Function to generate a random transaction
def generate_transaction(user_id):
    user = users[user_id]
    merchant = random.choice(merchants)
    amount = random.randint(50, 500)
    transaction_type = "debit" if random.random() > 0.1 else "credit"
    time_of_transaction = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Update account balance based on transaction type
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

# API endpoint to get transactions for a user
@app.route('/transactions', methods=['GET'])
def get_transactions():
    user_id = request.args.get('user_id', 'user1')  # Default user_id is 'user1'

    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    user = users[user_id]
    
    # Calculate the monthly spending (debits)
    now = datetime.datetime.now()
    current_month = now.month
    monthly_spent = sum(
        t["amount"] for t in user["transactions_history"]
        if t["type"] == "debit" and datetime.datetime.strptime(t["time"], "%Y-%m-%d %H:%M:%S").month == current_month
    )

    # Return the most recent transactions (50 latest)
    return jsonify({
        "balance": user["account_balance"],
        "transactions": user["transactions_history"][-50:],  # Latest 50 transactions
        "monthly_spent": monthly_spent,
        "monthly_budget": user["monthly_budget"]
    })

# API endpoint to set or update the budget for a user
@app.route('/set-budget', methods=['POST'])
def set_budget():
    user_id = request.json.get('user_id', 'user1')  # Default user_id is 'user1'
    budget = request.json.get('monthly_budget')

    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    if not budget or budget <= 0:
        return jsonify({"error": "Invalid budget value"}), 400

    users[user_id]["monthly_budget"] = budget
    return jsonify({"message": "Budget updated successfully"}), 200

# Function to generate transactions every 10 seconds (background thread)
def generate_transactions_periodically():
    while True:
        time.sleep(10)  # Generate a new transaction every 10 seconds
        generate_transaction('user1')  # Replace 'user1' with dynamic user ID if needed

if __name__ == '__main__':
    # Start the background thread for generating transactions periodically
    transaction_thread = Thread(target=generate_transactions_periodically)
    transaction_thread.daemon = True
    transaction_thread.start()

    # Start the Flask app
    app.run(host='0.0.0.0', port=10000)
