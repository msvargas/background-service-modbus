import threading
from flask import Flask, jsonify

app = Flask(__name__)

# Endpoint URL
@app.route('/getLastMeasurements', methods=['GET'])
def get_last_measurements():
    # Mock response
    response = {
        "detail": "ok",
        "result": [
            {
            "id": 1540,
            "value": 12.3,
            "created_at": "2024-10-02T20:40:15.112473",
            "measure_type": "ISOLATION",
            "detail": "opt3"
            },
            {
            "id": 1573,
            "value": 12.3,
            "created_at": "2024-10-02T20:40:22.112106",
            "measure_type": "RESISTANCE",
            "detail": "opt3"
            }
        ]
    }
    return jsonify(response)

def run_flask_app():
    app.run(host='0.0.0.0', port=8000)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()