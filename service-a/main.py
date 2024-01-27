# service_a/main.py
from flask import Flask
import requests
import schedule
import datetime
import time
import json
from threading import Thread
from collections import OrderedDict

app = Flask(__name__)
coin_values = []
current_value = OrderedDict({
    'coin': None,
    'value': None,
    'currency': None,
    'average_value': None,
    'timestamp': None
})

API_ENDPOINT = 'https://min-api.cryptocompare.com/data/price'


def fetch_coin_value(api_endpoint: str = API_ENDPOINT, coin: str = 'BTC', currency: str = 'USD') -> float:
    try:
        api_endpoint = f"{api_endpoint}?fsym={coin}&tsyms={currency}"
        response = requests.get(api_endpoint)
        response.raise_for_status()
        data = response.json()
        coin_value = data.get(currency)
        return coin_value
    except requests.exceptions.RequestException as e:
        return json.dumps({f"(value in {currency} (latest price since there are too many requests)": current_value}, indent=4)


def get_bitcoin_value(api_endpoint: str = API_ENDPOINT, coin: str = 'BTC', currency: str = 'USD'):
    try:
        with app.app_context():
            global current_value
            coin_value = fetch_coin_value(
                api_endpoint=api_endpoint, coin=coin, currency=currency)
            current_value['value'] = coin_value
            current_value['coin'] = coin
            current_value['currency'] = currency
            current_value['timestamp'] = datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')
            if coin_value is not None:
                print(f"Current {coin} Value (Service A): {current_value}")
                coin_values.append(coin_value)
                if len(coin_values) >= 10:
                    average_value = sum(coin_values) / len(coin_values)
                    print(
                        f"Average {coin} Value (Service A): {average_value} {currency} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    coin_values.clear()
                    current_value['average_value'] = average_value
                    return json.dumps(current_value, indent=4)
            else:
                print("Error fetching Bitcoin value")
                return json.dumps({f"error": "Failed to fetch {coin} value"}, indent=4)

            return json.dumps(current_value, indent=4)
    except Exception as e:
        print(e)
        return json.dumps({f"error": "Failed to fetch {coin} value"}, indent=4)


@app.route('/', methods=['GET'])
def index():
    return "Hello from Service A please use /service-a to get the coin value you want"


@app.route('/service-a', methods=['GET'])
def service_a():
    if current_value['average_value'] is None:
        current_value['average_value'] = 'No average value yet since there are not enough values to calculate it please wait a 10 minutes'
    return json.dumps(current_value, indent=4, separators=(',', ': '))


def main():
    # Schedule job every minute
    schedule.every(1).minutes.do(get_bitcoin_value)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    thread = Thread(target=main)
    thread.start()
    app.run(host='0.0.0.0', port=5000)
