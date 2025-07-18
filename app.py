import os
import json
import subprocess
import threading
import queue
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class MCPServer:
    def __init__(self):
        self.process = None
        self.output_queue = queue.Queue()
        self.start()
    
    def start(self):
        env = os.environ.copy()
        self.process = subprocess.Popen(
            ['uvx', 'mcp-google-sheets@latest'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            bufsize=0
        )
        
        # Thread pour lire les sorties
        threading.Thread(target=self._read_output, daemon=True).start()
        
        # Initialiser
        self._initialize()
    
    def _read_output(self):
        while self.process and self.process.poll() is None:
            line = self.process.stdout.readline()
            if line:
                self.output_queue.put(line.strip())
    
    def _initialize(self):
        init_cmd = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "0.1.0",
                "capabilities": {},
                "clientInfo": {"name": "elestio-wrapper", "version": "1.0.0"}
            },
            "id": 1
        }
        self.send_command(init_cmd)
        time.sleep(2)  # Attendre l'initialisation
    
    def send_command(self, command):
        try:
            self.process.stdin.write(json.dumps(command) + '\n')
            self.process.stdin.flush()
            
            # Attendre la réponse
            timeout = 5
            start = time.time()
            while time.time() - start < timeout:
                try:
                    line = self.output_queue.get(timeout=0.1)
                    if line.startswith('{'):
                        return json.loads(line)
                except queue.Empty:
                    continue
            
            return {"error": "Timeout"}
        except Exception as e:
            return {"error": str(e)}

# Instance globale
mcp_server = None

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "MCP Google Sheets"})

@app.route('/sheets/create', methods=['POST'])
def create_sheet():
    global mcp_server
    
    if not mcp_server:
        mcp_server = MCPServer()
    
    data = request.json
    title = data.get('title', 'New Sheet')
    
    command = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "create_spreadsheet",
            "arguments": {"title": title}
        },
        "id": 2
    }
    
    response = mcp_server.send_command(command)
    return jsonify(response)

@app.route('/sheets/<sheet_id>/read', methods=['GET'])
def read_sheet(sheet_id):
    global mcp_server
    
    if not mcp_server:
        mcp_server = MCPServer()
    
    command = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "get_sheet_data",
            "arguments": {
                "spreadsheet_id": sheet_id,
                "range": request.args.get('range', 'A1:Z1000')
            }
        },
        "id": 3
    }
    
    response = mcp_server.send_command(command)
    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8003))
    app.run(host='0.0.0.0', port=port)
