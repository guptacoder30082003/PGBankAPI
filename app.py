from flask import Flask, jsonify, request
import random
import datetime

app = Flask(__name__)

# Simulated user data
users = {
    "user1": {
        "account_balance": 10000,
        "monthly_budget": 10000,
        "transactions_history": []
    }
}

# List of sample merchants
merchants = ["Amazon", "Flipkart", "Swiggy", "Zomato", "Uber", "Google Play", "Paytm", "Netflix"]

# Function to create 1 new transaction
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

# Create a new transaction and return latest data
def get_transaction_data(user_id='user1'):
    if user_id not in users:
        return {"error": "User not found"}, 404

    transaction = generate_transaction(user_id)
    user = users[user_id]

    return {
        "balance": user["account_balance"],
        "transaction": transaction,
        "monthly_budget": user["monthly_budget"]
    }

# Root route ("/") returns latest data
@app.route('/')
def home():
    data = get_transaction_data()
    if isinstance(data, tuple):
        return jsonify(data[0]), data[1]
    return jsonify(data)

# Same for "/transactions" if frontend uses it
@app.route('/transactions', methods=['GET'])
def get_transactions():
    user_id = request.args.get('user_id', 'user1')
    data = get_transaction_data(user_id)
    if isinstance(data, tuple):
        return jsonify(data[0]), data[1]
    return jsonify(data)

# Let frontend (dashboard) set the monthly budget
@app.route('/set-budget', methods=['POST'])
def set_budget():
    user_id = request.json.get('user_id', 'user1')
    budget = request.json.get('monthly_budget')

    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    if not budget or budget <= 0:
        return jsonify({"error": "Invalid budget value"}), 400

    users[user_id]["monthly_budget"] = budget
    return jsonify({"message": "Budget updated successfully"}), 200

# Start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
