# service-b/main.py
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/display_bitcoin_info', methods=['GET'])
def display_bitcoin_info():
    # Assuming service-b is calling service-a to get the Bitcoin information
    # Adjust the URL and headers as needed based on your actual service-a API
    service_a_url = 'http://service-a-service-a.default.svc.cluster.local:5000/current_bitcoin_value'
    response = requests.get(service_a_url)

    if response.status_code == 200:
        bitcoin_info = response.json()
        return jsonify({"service_b_display": bitcoin_info})
    else:
        return jsonify({"service_b_display": "Error getting Bitcoin information from Service A"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
