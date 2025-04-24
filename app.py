from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import datetime
from collections import defaultdict

app = Flask(__name__)
CORS(app)

# User data storage with transaction history
users = {
    "default_user": {
        "account_balance": 10000,
        "monthly_budget": 10000,
        "transactions_history": [],
        "total_debit": 0
    }
}

merchants = ["Amazon", "Flipkart", "Swiggy", "Zomato", "Uber", "Google Play", "Paytm", "Netflix"]

def generate_transaction(user_id):
    user = users[user_id]
    merchant = random.choice(merchants)
    amount = random.randint(50, 500)
    transaction_type = "debit" if random.random() > 0.1 else "credit"  # 90% debit, 10% credit
    time_of_transaction = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if transaction_type == "debit":
        if user["account_balance"] >= amount:  # Check sufficient balance
            user["account_balance"] -= amount
            user["total_debit"] += amount
        else:
            return None  # Return None for insufficient balance

    transaction = {
        "merchant": merchant,
        "amount": amount,
        "type": transaction_type,
        "time": time_of_transaction
    }

    user["transactions_history"].append(transaction)
    # Keep only last 5 transactions
    user["transactions_history"] = user["transactions_history"][-5:]
    return transaction

@app.route('/', methods=['GET', 'POST'])
def home():
    user = users["default_user"]
    
    if request.method == 'POST':
        data = request.get_json()
        if 'account_balance' in data:
            user['account_balance'] = float(data['account_balance'])
        if 'monthly_budget' in data:
            user['monthly_budget'] = float(data['monthly_budget'])
    
    new_transaction = generate_transaction("default_user")
    
    return jsonify({
        "balance": user["account_balance"],
        "monthly_budget": user["monthly_budget"],
        "total_debit": user["total_debit"],
        "transactions": user["transactions_history"][::-1],  # Return newest first
        "new_transaction": new_transaction
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
