from flask import Flask, jsonify
import random
import datetime

app = Flask(__name__)

account_balance = 10000  

merchants = ["Amazon", "Flipkart", "Swiggy", "Zomato", "Uber", "Google Play", "Paytm", "Netflix"]

def generate_transaction():
    global account_balance
    merchant = random.choice(merchants)
    amount = random.randint(50, 500)  # Random transaction amount
    transaction_type = "debit" if random.random() > 0.1 else "credit"  # Mostly debit
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if transaction_type == "debit":
        account_balance -= amount  
    else:
        account_balance += amount  
    return {
        "merchant": merchant,
        "amount": amount,
        "type": transaction_type,
        "time": time
    }

@app.route('/')
def home():
    transaction = generate_transaction()  # Generate a new transaction
    return jsonify({
        "balance": account_balance,
        "latest_transaction": transaction
    })

@app.route('/balance', methods=['GET'])
def get_balance():
    return jsonify({"balance": account_balance})

@app.route('/transactions', methods=['GET'])
def get_transaction():
    transaction = generate_transaction()
    return jsonify(transaction)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
