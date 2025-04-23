from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import datetime
from threading import Thread
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize with sample data
account_balance = 10000
transactions_history = []
monthly_spent = 0

merchants = ["Amazon", "Flipkart", "Swiggy", "Zomato", "Uber", "Google Play", "Paytm", "Netflix"]

def generate_transaction():
    global account_balance, monthly_spent
    merchant = random.choice(merchants)
    amount = random.randint(50, 500)
    transaction_type = "debit" if random.random() > 0.1 else "credit"
    time_of_transaction = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if transaction_type == "debit":
        account_balance -= amount
        monthly_spent += amount
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
    # Return last 50 transactions and current balance
    return jsonify({
        "balance": account_balance,
        "monthly_spent": monthly_spent,
        "transactions": transactions_history[-50:]  # Return recent transactions
    })

@app.route('/monthly-spending', methods=['GET'])
def get_monthly_spending():
    # Simulate weekly spending data
    return jsonify({
        "labels": ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        "data": [random.randint(1000, 3000) for _ in range(4)]
    })

@app.route('/top-merchants', methods=['GET'])
def get_top_merchants():
    # Simulate top merchants data
    top_merchants = random.sample(merchants, 5)
    return jsonify({
        "labels": top_merchants,
        "data": [random.randint(500, 3500) for _ in range(5)]
    })

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
