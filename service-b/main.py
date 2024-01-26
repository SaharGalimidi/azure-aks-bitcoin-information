# service_b/main.py
from flask import Flask, jsonify
import requests
import datetime


app = Flask(__name__)

API_ENDPOINT = 'https://api.coingecko.com/api/v3/simple/price'


@app.route('/', methods=['GET'])
def index():
    return "Hello from Service B please use /service-b to get the coin value you want"


@app.route('/service-b', methods=['GET'])
def get_service_a_data(coin: str = 'bitcoin', currency: str = 'usd'):
    try:
        params = {'ids': coin, 'vs_currencies': currency}
        response = requests.get(API_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()
        coin_value = data.get(coin).get(currency)
        print(
            f"Current {coin} Value (Service B): {coin_value} {currency} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return jsonify({coin: coin_value, "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching data from Service B: {e}"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
