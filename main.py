import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Put your actual Gumroad Access Token here (make sure it's the new one!)
GUMROAD_TOKEN = "PASTE_YOUR_NEW_GUMROAD_ACCESS_TOKEN_HERE" 

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    license_key = data.get('license_key', '').strip()
    
    if not license_key:
        return jsonify({"status": "error", "message": "No key provided."}), 400
        
    try:
        # FIX: Added product_permalink back in. Gumroad needs to know which product this is for!
        # FIX: increment_uses_count=false stops Gumroad from locking your test key.
        resp = requests.post(
            "https://api.gumroad.com/v2/licenses/verify",
            data={
                "product_permalink": "kvrccx", 
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
