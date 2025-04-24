from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import datetime

app = Flask(__name__)
CORS(app)

users = {
    "default_user": {
        "account_balance": 10000,
        "monthly_budget": 10000,
        "transactions_history": []
    }
}

merchants = ["Amazon", "Flipkart", "Swiggy", "Zomato", "Uber", "Google Play", "Paytm", "Netflix"]

def generate_transaction(user_id):
    user = users[user_id]
    merchant = random.choice(merchants)
    amount = random.randint(50, 500)
    # 90% chance of debit, 10% chance of credit
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

    # Only keep the most recent transaction
    user["transactions_history"] = [transaction]
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
        "transaction": new_transaction  # Only returning the single transaction
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
