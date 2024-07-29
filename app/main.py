import threading
from flask import Flask, jsonify

app = Flask(__name__)
# Endpoint URL
ENDPOINT_URL = "http://localhost:8000/getLastMeasurements"

@app.route('/getLastMeasurements', methods=['GET'])
def get_last_measurements():
    # Mock response
    response = {
        "temperature": None,
        "resistance": {
            "id": 6,
            "value": 7,
            "type": "3",
            "created_at": "2024-07-10T22:51:14+00:00"
        },
        "vibration": None,
        "isolation": {
            "id": 8,
            "value": 1256,
            "type": None,
            "created_at": "2024-07-09T14:33:47+00:00"
        },
        "pressure": None
    }
    return jsonify(response)

def run_flask_app():
    app.run(host='0.0.0.0', port=8000)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()