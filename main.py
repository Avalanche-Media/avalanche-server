import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

GUMROAD_TOKEN = "Bkp1ceKc8O5XPtZS01ZUbnQo3GzDLOTUfHIxy1lkgxs" 
GUMROAD_PERMALINK = "kvrccx"

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    license_key = data.get('license_key', '').strip()
    
    if not license_key:
        return jsonify({"status": "error", "message": "No key provided."}), 400
        
    try:
        resp = requests.post(
            "https://api.gumroad.com/v2/licenses/verify",
            data={
                "product_permalink": GUMROAD_PERMALINK, 
                "license_key": license_key, 
                "increment_uses_count": "false"
            },
            auth=(GUMROAD_TOKEN, ""), 
            timeout=10
        )
        
        # FIX: Return Gumroad's EXACT response so we can see why it's failing
        return jsonify(resp.json())

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
