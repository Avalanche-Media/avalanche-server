import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# SECURITY: Put your Gumroad Access Token here. It is safe on this server!
GUMROAD_TOKEN = "RVBxQnrigF2-KSZ0pG25Og==" 

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    license_key = data.get('license_key', '').strip()
    
    if not license_key:
        return jsonify({"status": "error", "message": "No key provided."}), 400
        
    try:
        # We send the key to Gumroad. 
        # increment_uses_count="false" stops Gumroad from locking your key when you test it multiple times.
        resp = requests.post(
            "https://api.gumroad.com/v2/licenses/verify",
            data={"license_key": license_key, "increment_uses_count": "false"},
            auth=(GUMROAD_TOKEN, ""), 
            timeout=10
        ).json()
        
        # Gumroad replies with "success": true if the key is real and not refunded.
        is_valid = resp.get('success', False) and not resp.get('purchase', {}).get('refunded', False)
        
        if is_valid:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "Invalid or refunded key."}), 403
            
    except Exception as e:
        return jsonify({"status": "error", "message": "Server error."}), 500

# FIX: This is the part that stops Render from crashing!
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
