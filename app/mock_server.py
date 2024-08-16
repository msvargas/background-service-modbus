import threading
from flask import Flask, jsonify

app = Flask(__name__)

# Endpoint URL
@app.route('/getLastMeasurements', methods=['GET'])
def get_last_measurements():
    # Mock response
    response = {
        "temperature":  {
            "id": 5,
            "value": 3000,
            "type": "3",
            "created_at": "2024-07-10T22:51:14+00:00"
        },
        "resistance": {
            "id": 1,
            "value": 36789,
            "type": "3",
            "created_at": "2024-07-10T22:51:14+00:00"
        },
        "vibration":  {
            "id": 4,
            "value": 1256,
            "type": 3,
            "created_at": "2024-07-09T14:33:47+00:00"
        },
        "isolation": {
            "id": 2,
            "value": 62090,
            "type": 3,
            "created_at": "2024-07-09T14:33:47+00:00"
        },
        "pressure":  {
            "id": 3,
            "value": 19234,
            "type": 3,
            "created_at": "2024-07-09T14:33:47+00:00"
        }
    }
    return jsonify(response)

def run_flask_app():
    app.run(host='0.0.0.0', port=8000)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()