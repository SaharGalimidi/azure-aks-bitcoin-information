# service_a/main.py
from flask import Flask, jsonify
import requests
import schedule
import datetime
import time
from threading import Thread

app = Flask(__name__)
coin_values = []

last_btc_price = ""

API_ENDPOINT = 'https://api.coingecko.com/api/v3/simple/price'


def fetch_coin_value(api_endpoint: str = API_ENDPOINT, coin: str = 'bitcoin', currency: str = 'usd') -> float:
    try:
        global last_btc_price
        api_endpoint = f"{api_endpoint}?ids={coin}&vs_currencies={currency}"
        response = requests.get(api_endpoint)
        response.raise_for_status()
        data = response.json()
        coin_value = data.get(coin).get(currency)
        last_btc_price = coin_value
        return coin_value
    except requests.exceptions.RequestException as e:
        return {f"(value in {currency} (latest price since there are too many requests)": last_btc_price}


@app.route('/', methods=['GET'])
def index():
    return "Hello from Service A please use /service-a to get the coin value you want"


def get_bitcoin_value(api_endpoint: str = API_ENDPOINT, coin: str = 'bitcoin', currency: str = 'usd'):
    try:
        with app.app_context():
            coin_value = fetch_coin_value(
                api_endpoint=api_endpoint, coin=coin, currency=currency)

            if coin_value is not None:
                print(
                    f"Current {coin} Value (Service A): {coin_value} {currency} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                coin_values.append(coin_value)

                if len(coin_values) >= 10:
                    average_value = sum(coin_values) / len(coin_values)
                    print(
                        f"Average {coin} Value (Service A): {average_value} {currency} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    coin_values.clear()
                    return jsonify({coin: str(coin_value) + f" {currency}", f"average {coin}": str(average_value) + f" {currency}", "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            else:
                print("Error fetching Bitcoin value")
                # Return an error response
                return jsonify({f"error": "Failed to fetch {coin} value"}), 500

            return jsonify({coin: str(coin_value) + f" {currency}", "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    except Exception as e:
        print(e)
        return jsonify({f"error": "Failed to fetch {coin} value"}), 500


@app.route('/service-a', methods=['GET'])
def service_a():
    return get_bitcoin_value()


def main():
    # Schedule job every minute
    schedule.every(1).minutes.do(get_bitcoin_value)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    # Run main function in a separate thread
    thread = Thread(target=main)
    thread.start()

    # Start Flask server
    # Allow connections from all network interfaces
    app.run(host='0.0.0.0', port=5000)
