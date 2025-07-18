from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "MCP Google Sheets Server", "status": "running"})

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = 8003
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)
