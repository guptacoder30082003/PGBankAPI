from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import datetime
import time
from collections import defaultdict

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# User data storage
users = {
    "default_user": {
        "account_balance": 10000,  # Default starting balance
        "monthly_budget": 10000,   # Default monthly budget
        "transactions_history": [],
        "last_fetch_time": None
    }
}

merchants = ["Amazon", "Flipkart", "Swiggy", "Zomato", "Uber", "Google Play", "Paytm", "Netflix"]

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

@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    user_id = "default_user"
    user = users[user_id]

    # Update user data if POST request
    if request.method == 'POST':
        data = request.get_json()
        if 'account_balance' in data:
            user['account_balance'] = float(data['account_balance'])
        if 'monthly_budget' in data:
            user['monthly_budget'] = float(data['monthly_budget'])

    # Generate a new transaction on each fetch
    new_transaction = generate_transaction(user_id)
    
    # Calculate monthly spending
    now = datetime.datetime.now()
    current_month = now.month
    monthly_spent = sum(
        t["amount"] for t in user["transactions_history"]
        if t["type"] == "debit" and 
        datetime.datetime.strptime(t["time"], "%Y-%m-%d %H:%M:%S").month == current_month
    )

    # Prepare response
    response = {
        "balance": user["account_balance"],
        "monthly_budget": user["monthly_budget"],
        "monthly_spent": monthly_spent,
        "transactions": user["transactions_history"][-50:],  # Last 50 transactions
        "new_transaction": new_transaction
    }

    return jsonify(response)

if __name__ == '__main__':
    # Generate initial transactions
    for _ in range(5):
        generate_transaction("default_user")
    
    app.run(host='0.0.0.0', port=10000, debug=True)
