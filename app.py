from flask import Flask, jsonify, request
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "MCP Google Sheets API", "status": "ready"})

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/sheets/create', methods=['POST'])
def create_sheet():
    # Ici on pourrait appeler le serveur MCP
    data = request.json
    return jsonify({
        "success": True,
        "message": f"Sheet '{data.get('title', 'New Sheet')}' would be created",
        "note": "MCP integration pending"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003)
