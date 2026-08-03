import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Put your Gumroad Access Token here
GUMROAD_TOKEN = "Bkp1ceKc8O5XPtZS01ZUbnQo3GzDLOTUfHIxy1lkgxs" 

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    license_key = data.get('license_key', '').strip()
    
    if not license_key:
        return jsonify({"status": "error", "message": "No key provided."}), 400
        
    try:
        # FIX: Removed the product_id completely! Gumroad will just check the key against your account.
        # FIX: Added increment_uses_count=false so Gumroad doesn't lock your test key.
        resp = requests.post(
            "https://api.gumroad.com/v2/licenses/verify",
            data={"license_key": license_key, "increment_uses_count": "false"},
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
