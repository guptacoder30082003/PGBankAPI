from flask import Flask, jsonify
import random
import datetime
from threading import Thread
import time
from bs4 import BeautifulSoup

app = Flask(__name__)
account_balance = 10000  # Default balance, will be updated from dashboard.html
merchants = ["Amazon", "Flipkart", "Swiggy", "Zomato", "Uber", "Google Play", "Paytm", "Netflix"]
def generate_transaction():
    global account_balance
    merchant = random.choice(merchants)
    amount = random.randint(50, 500)  # Random transaction amount
    transaction_type = "debit" if random.random() > 0.1 else "credit"  # Mostly debit
    time_of_transaction = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if transaction_type == "debit":
        account_balance -= amount  
    else:
        account_balance += amount  
    return {
        "merchant": merchant,
        "amount": amount,
        "type": transaction_type,
        "time": time_of_transaction
    }
def read_balance_from_html():
    global account_balance
    today = datetime.datetime.now()
    if today.day == 1: 
        try:
            with open('dashboard.html', 'r') as file:
                html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            balance_element = soup.find(id="account_balance")
            if balance_element:
                # Extract the balance as a number
                account_balance = float(balance_element.text.strip())
            else:
                print("Balance element not found in the HTML.")
        except Exception as e:
            print(f"Error reading the HTML file: {e}")

def generate_transactions_periodically():
    while True:
        time.sleep(10)  
        generate_transaction()

@app.route('/')
def home():
    transaction = generate_transaction()  
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
    # Read balance from dashboard.html on the 1st day of the month
    read_balance_from_html()
    # Start the background thread to generate transactions every 10 seconds
    transaction_thread = Thread(target=generate_transactions_periodically)
    transaction_thread.daemon = True  # Ensure the thread terminates when the main program ends
    transaction_thread.start()
    app.run(debug=True, host='0.0.0.0', port=10000)
