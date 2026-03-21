from flask import Flask, jsonify
from flask_cors import CORS
import datetime
import os

app = Flask(__name__)
CORS(app) # Esto es vital para que el Frontend pueda hablar con el Backend

@app.route('/api/health')
def health():
    return jsonify({
        "status": "online",
        "system": "VAULT LOGIC GENESIS",
        "timestamp": datetime.datetime.now().isoformat(),
        "nasa_sync": "ACTIVE",
        "latency": "12ms"
    })

@app.route('/api/orbital-data')
def orbital_data():
    return jsonify({
        "epoch": "J2000.0",
        "reference": "DE441",
        "vectors": {
            "sun": [0.0, 0.0, 0.0],
            "earth": [0.983, 0.123, 0.001],
            "jupiter": [5.203, -0.456, 0.023]
        },
        "market_sync_score": 0.9847
    })

if __name__ == "__main__":
    # Esto permite que corra localmente y en Render usando el puerto que ellos asignen
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
