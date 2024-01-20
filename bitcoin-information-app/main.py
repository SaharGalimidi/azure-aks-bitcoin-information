from flask import Flask, jsonify
import requests
import schedule
import time

app = Flask(__name__)
bitcoin_values = []

def fetch_bitcoin_value(api_endpoint):
    try:
        response = requests.get(api_endpoint)
        response.raise_for_status()
        data = response.json()
        bitcoin_value = data.get('bitcoin').get('usd') 
        return bitcoin_value
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Bitcoin value: {e}")
        return None

def job():
    global bitcoin_values
    bitcoin_value = fetch_bitcoin_value('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')  

    if bitcoin_value is not None:
        print(f"Current Bitcoin Value: {bitcoin_value}")
        bitcoin_values.append(bitcoin_value)

def calculate_average():
    global bitcoin_values
    if bitcoin_values:
        average_value = sum(bitcoin_values) / len(bitcoin_values)
        print(f"Average Bitcoin Value (last 10 minutes): {average_value}")
        bitcoin_values = []  # Reset the list for the next 10 minutes

@app.route('/current_bitcoin_value', methods=['GET'])
def get_current_bitcoin_value():
    bitcoin_value = fetch_bitcoin_value('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
    return jsonify({"current_bitcoin_value": bitcoin_value})

@app.route('/average_bitcoin_value', methods=['GET'])
def get_average_bitcoin_value():
    global bitcoin_values
    calculate_average()
    return jsonify({"average_bitcoin_value": sum(bitcoin_values) / len(bitcoin_values)})

def main():
    # Schedule job every minute
    schedule.every(1).minutes.do(job)

    # Schedule average calculation every 10 minutes
    schedule.every(10).minutes.do(calculate_average)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
