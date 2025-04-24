from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import datetime
from collections import defaultdict

app = Flask(__name__)
CORS(app)

users = {
    "default_user": {
        "account_balance": 10000,
        "monthly_budget": 10000,
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

@app.route('/')
def home():
    user = users["default_user"]
    last_transaction = user["transactions_history"][-1] if user["transactions_history"] else None
    
    now = datetime.datetime.now()
    current_month = now.month
    monthly_spent = sum(
        t["amount"] for t in user["transactions_history"]
        if t["type"] == "debit" and 
        datetime.datetime.strptime(t["time"], "%Y-%m-%d %H:%M:%S").month == current_month
    )

    return jsonify({
        "balance": user["account_balance"],
        "monthly_budget": user["monthly_budget"],
        "monthly_spent": monthly_spent,
        "last_transaction": last_transaction,
        "transaction_count": len(user["transactions_history"])
    })

@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    user_id = "default_user"
    user = users[user_id]

    if request.method == 'POST':
        data = request.get_json()
        if 'account_balance' in data:
            user['account_balance'] = float(data['account_balance'])
        if 'monthly_budget' in data:
            user['monthly_budget'] = float(data['monthly_budget'])

    new_transaction = generate_transaction(user_id)
    
    now = datetime.datetime.now()
    current_month = now.month
    monthly_spent = sum(
        t["amount"] for t in user["transactions_history"]
        if t["type"] == "debit" and 
        datetime.datetime.strptime(t["time"], "%Y-%m-%d %H:%M:%S").month == current_month
    )

    response = {
        "balance": user["account_balance"],
        "monthly_budget": user["monthly_budget"],
        "monthly_spent": monthly_spent,
        "transactions": user["transactions_history"][-50:],
        "new_transaction": new_transaction
    }

    return jsonify(response)

if __name__ == '__main__':
    for _ in range(5):
        generate_transaction("default_user")
    app.run(host='0.0.0.0', port=10000, debug=True)
