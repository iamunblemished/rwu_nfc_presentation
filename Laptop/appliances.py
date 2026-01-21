from flask import Flask, request, jsonify

app = Flask(__name__)

# This script acts as a generic "Listener" for any IoT event fired by your Pi
@app.route('/node/alpha', methods=['POST'])
def node_alpha():
    data = request.json
    user = data.get("user", "Unknown")
    print(f"\n[NODE ALPHA] Event Received!")
    print(f" > Source: Raspberry Pi Server")
    print(f" > Identity: {user}")
    print(f" > Command: INITIALIZE_STATE_ACTIVE")
    return jsonify({"status": "acknowledged", "node": "alpha"}), 200

@app.route('/node/beta', methods=['POST'])
def node_beta():
    data = request.json
    user = data.get("user", "Unknown")
    print(f"\n[NODE BETA] Event Received!")
    print(f" > Source: Raspberry Pi Server")
    print(f" > Identity: {user}")
    print(f" > Command: TRIGGER_PERIPHERAL_SYNC")
    return jsonify({"status": "acknowledged", "node": "beta"}), 200

if __name__ == "__main__":
    # Ensure this port matches what you put in your Pi's views.py
    print("--- IoT Ecosystem Simulator Active ---")
    print("Listening for Webhooks from Raspberry Pi...")
    app.run(host='0.0.0.0', port=5000)