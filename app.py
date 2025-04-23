from flask import Flask, jsonify
import random
import datetime
from threading import Thread
import time

app = Flask(__name__)

account_balance = 10000
transactions_history = []

merchants = ["Amazon", "Flipkart", "Swiggy", "Zomato", "Uber", "Google Play", "Paytm", "Netflix"]

monthly_budget = 10000  # Can be dynamic per user

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
    # Calculate total debit (monthly_spent)
    now = datetime.datetime.now()
    current_month = now.month
    monthly_spent = sum(
        t["amount"] for t in transactions_history
        if t["type"] == "debit" and datetime.datetime.strptime(t["time"], "%Y-%m-%d %H:%M:%S").month == current_month
    )

    # Return the most recent transactions (50 latest)
    return jsonify({
        "balance": account_balance,
        "transactions": transactions_history[-50:],
        "monthly_spent": monthly_spent,
        "monthly_budget": monthly_budget
    })

def generate_transactions_periodically():
    while True:
        time.sleep(10)  # Generate a new transaction every 10 seconds
        generate_transaction()

if __name__ == '__main__':
    # Initial set of transactions (optional)
    for _ in range(5):
        generate_transaction()

    # Start the background thread for generating transactions periodically
    transaction_thread = Thread(target=generate_transactions_periodically)
    transaction_thread.daemon = True
    transaction_thread.start()

    # Start the Flask app
    app.run(host='0.0.0.0', port=10000)
