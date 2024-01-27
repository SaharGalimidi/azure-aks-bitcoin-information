# service_b/main.py
from flask import Flask, jsonify
import requests
import datetime
import json
from collections import OrderedDict
app = Flask(__name__)

API_ENDPOINT = 'https://min-api.cryptocompare.com/data/price'


@app.route('/', methods=['GET'])
def check_pod_health():
    return "Hello from Service B im healthy"

@app.route('/service-b', methods=['GET'])
def get_service_a_data(coin: str = 'BTC', currency: str = 'USD'):
    try:
        with app.app_context():
            end_point = f"{API_ENDPOINT}?fsym={coin}&tsyms={currency}"
            response = requests.get(end_point)
            response.raise_for_status()
            data = response.json()
            coin_value = data.get('USD')
            print(f"Current {coin} Value (Service B): {coin_value} {currency} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            order_info = OrderedDict([('coin', coin), 
                                      ('value', coin_value),
                                      ('currency', currency), 
                                      ('timestamp', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))])
            
            return json.dumps(order_info, indent=4)
    except requests.exceptions.RequestException as e:
        return json.dumps({f"({coin} value in {currency} (latest price since there are too many requests)": coin_value}, indent=4)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
