from flask import Flask, jsonify, request, redirect
import logging
import os
from consistent_hashing import ConsistentHashRing

# Configure logging
if not os.path.exists('app.log'):
    open('app.log', 'a').close()

logging.basicConfig(filename='app.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Logging is set up.")

app = Flask(__name__)

# Initialize consistent hashing ring
nodes = ["Server1", "Server2", "Server3"]
hash_ring = ConsistentHashRing(nodes)
server_ports = {
    "Server1": "5001",
    "Server2": "5002",
    "Server3": "5003"
}

# Helper function to get server ID based on IP address
def get_server_id():
    return hash_ring.get_node(request.remote_addr)

# Endpoint /home
@app.route('/home', methods=['GET'])
def home():
    server_id = get_server_id()
    return jsonify({
        "message": f"Hello from {server_id}",
        "status": "successful"
    }), 200

# Endpoint /heartbeat
@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    server_id = get_server_id()
    return jsonify({
        "message": f"Heartbeat from {server_id}",
        "status": "successful"
    }), 200

# Endpoint /rep
@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({
        "message": {
            "N": len(nodes),
            "replicas": nodes
        },
        "status": "successful"
    }), 200

# Endpoint /add
@app.route('/add', methods=['POST'])
def add_server():
    data = request.json
    new_nodes = data.get('hostnames', [])
    for node in new_nodes:
        if node not in nodes:
            nodes.append(node)
            hash_ring.add_node(node)
    return jsonify({
        "message": {
            "N": len(nodes),
            "replicas": nodes
        },
        "status": "successful"
    }), 200

# Endpoint /rm
@app.route('/rm', methods=['DELETE'])
def remove_server():
    data = request.json
    remove_nodes = data.get('hostnames', [])
    for node in remove_nodes:
        if node in nodes:
            nodes.remove(node)
            hash_ring.remove_node(node)
    return jsonify({
        "message": {
            "N": len(nodes),
            "replicas": nodes
        },
        "status": "successful"
    }), 200

# Route requests to the appropriate server based on consistent hashing
@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    server_id = hash_ring.get_node(request.remote_addr)
    server_port = server_ports.get(server_id)
    
    if server_port:
        logging.info(f"Routing request for {path} to {server_id}")
        # Construct the redirect URL based on the server's port
        redirect_url = f"http://localhost:{server_port}/{path}"
        return redirect(redirect_url, code=307)
    else:
        logging.error(f"Server {server_id} not found for routing request")
        return jsonify({
            "message": "Server not found",
            "status": "failed"
        }), 500


# Route requests to Server1
@app.route('/server1', methods=['GET'])
def server1_info():
    server_id = "Server1"
    server_port = server_ports.get(server_id)
    if server_port:
        return jsonify({
            "message": f"Information from {server_id}",
            "port": server_port,
            "status": "successful"
        }), 200
    else:
        return jsonify({
            "message": f"Server {server_id} not found",
            "status": "failed"
        }), 404

# Route requests to Server2
@app.route('/server2', methods=['GET'])
def server2_info():
    server_id = "Server2"
    server_port = server_ports.get(server_id)
    if server_port:
        return jsonify({
            "message": f"Information from {server_id}",
            "port": server_port,
            "status": "successful"
        }), 200
    else:
        return jsonify({
            "message": f"Server {server_id} not found",
            "status": "failed"
        }), 404

# Route requests to Server3
@app.route('/server3', methods=['GET'])
def server3_info():
    server_id = "Server3"
    server_port = server_ports.get(server_id)
    if server_port:
        return jsonify({
            "message": f"Information from {server_id}",
            "port": server_port,
            "status": "successful"
        }), 200
    else:
        return jsonify({
            "message": f"Server {server_id} not found",
            "status": "failed"
        }), 404

if __name__ == '__main__':
    logging.info("Flask app is starting.")
    app.run(host='0.0.0.0', port=5000)
