import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Your secret token is NOW safe on the server, not in the user's app!
GUMROAD_TOKEN = "NS6dofqgbS_S_9b3yDJ3qZM4kKtMiT8mMyHkiknh0uA" 
GUMROAD_PRODUCT_ID = "seqts"

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    license_key = data.get('license_key', '').strip()
    
    if not license_key:
        return jsonify({"status": "error", "message": "No key provided."}), 400
        
    try:
        resp = requests.post(
            "https://api.gumroad.com/v2/licenses/verify",
            data={"product_id": GUMROAD_PRODUCT_ID, "license_key": license_key},
            auth=(GUMROAD_TOKEN, ""), timeout=10
        ).json()
        
        is_valid = resp.get('success', False) and not resp.get('purchase', {}).get('refunded', False)
        
        if is_valid:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "Invalid or refunded key."}), 403
            
    except Exception as e:
        return jsonify({"status": "error", "message": "Server error."}), 500

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
