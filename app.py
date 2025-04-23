from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import datetime
from threading import Thread
import time
from collections import defaultdict

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize with sample data
account_balance = 10000
transactions_history = []
monthly_budget = 10000  # Default budget

merchants = ["Amazon", "Flipkart", "Swiggy", "Zomato", "Uber", "Google Play", "Paytm", "Netflix"]

def generate_transaction():
    global account_balance
    merchant = random.choice(merchants)
    amount = random.randint(50, 500)
    transaction_type = "debit" if random.random() > 0.1 else "credit"
    time_of_transaction = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if transaction_type == "debit":
        account_balance -= amount
    else:
        account_balance += amount
    
    transaction = {
        "merchant": merchant,
        "amount": amount,
        "type": transaction_type,
        "time": time_of_transaction
    }
    
    transactions_history.append(transaction)
    return transaction

@app.route('/transactions', methods=['GET'])
def get_transactions():
    # Calculate monthly spending for the current month
    now = datetime.datetime.now()
    current_month = now.month
    monthly_spent = sum(
        t["amount"] for t in transactions_history
        if t["type"] == "debit" and 
        datetime.datetime.strptime(t["time"], "%Y-%m-%d %H:%M:%S").month == current_month
    )
    
    # Return last 50 transactions and current balance
    return jsonify({
        "balance": account_balance,
        "monthly_spent": monthly_spent,
        "monthly_budget": monthly_budget,
        "transactions": transactions_history[-50:]  # Return recent transactions
    })

@app.route('/monthly-spending', methods=['GET'])
def get_monthly_spending():
    # Calculate weekly spending for the current month
    now = datetime.datetime.now()
    current_month = now.month
    
    # Group transactions by week
    weekly_spending = [0, 0, 0, 0]  # Initialize for 4 weeks
    
    for t in transactions_history:
        if t["type"] == "debit":
            trans_date = datetime.datetime.strptime(t["time"], "%Y-%m-%d %H:%M:%S")
            if trans_date.month == current_month:
                week_num = (trans_date.day - 1) // 7
                if week_num < 4:  # Only consider first 4 weeks
                    weekly_spending[week_num] += t["amount"]
    
    return jsonify({
        "labels": ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        "data": weekly_spending
    })

@app.route('/top-merchants', methods=['GET'])
def get_top_merchants():
    # Calculate spending by merchant for the current month
    now = datetime.datetime.now()
    current_month = now.month
    merchant_spending = defaultdict(int)
    
    for t in transactions_history:
        if t["type"] == "debit":
            trans_date = datetime.datetime.strptime(t["time"], "%Y-%m-%d %H:%M:%S")
            if trans_date.month == current_month:
                merchant_spending[t["merchant"]] += t["amount"]
    
    # Get top 5 merchants
    top_merchants = sorted(merchant_spending.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return jsonify({
        "labels": [m[0] for m in top_merchants],
        "data": [m[1] for m in top_merchants]
    })

@app.route('/set-budget', methods=['POST'])
def set_budget():
    global monthly_budget
    data = request.get_json()
    monthly_budget = data.get('budget', monthly_budget)
    return jsonify({"status": "success", "monthly_budget": monthly_budget})

def generate_transactions_periodically():
    while True:
        time.sleep(10)
        generate_transaction()

if __name__ == '__main__':
    # Pre-populate with some transactions
    for _ in range(5):
        generate_transaction()
    
    # Start background thread
    transaction_thread = Thread(target=generate_transactions_periodically)
    transaction_thread.daemon = True
    transaction_thread.start()
    
    app.run(host='0.0.0.0', port=10000)
