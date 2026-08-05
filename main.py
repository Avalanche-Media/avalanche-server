import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1. Paste your REAL Access Token here (from Gumroad Settings -> Advanced -> API)
GUMROAD_TOKEN = "Bkp1ceKc8O5XPtZS01ZUbnQo3GzDLOTUfHIxy1lkgxs" 

# 2. Paste your REAL Product ID here (from the web address bar when editing your product)
GUMROAD_PRODUCT_ID = "kvrccx"

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    license_key = data.get('license_key', '').strip()
    
    if not license_key:
        return jsonify({"status": "error", "message": "No key provided."}), 400
        
    try:
        # We send the Product ID, the license key, and tell Gumroad not to lock the test key
        resp = requests.post(
            "https://api.gumroad.com/v2/licenses/verify",
            data={
                "product_id": GUMROAD_PRODUCT_ID, 
                "license_key": license_key, 
                "increment_uses_count": "false"
            },
            auth=(GUMROAD_TOKEN, ""), 
            timeout=10
        ).json()
        
        is_valid = resp.get('success', False) and not resp.get('purchase', {}).get('refunded', False)
        
        if is_valid:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "Invalid or refunded key."}), 403
            
    except Exception as e:
        return jsonify({"status": "error", "message": "Server error."}), 500

# This part stops Render from crashing!
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
