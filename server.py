from flask import Flask, jsonify, request
import os
from consistent_hashing import ConsistentHashRing

app = Flask(__name__)

# Initialize consistent hashing ring
nodes = ["Server1", "Server2", "Server3"]
hash_ring = ConsistentHashRing(nodes)

# Endpoint /home
@app.route('/home', methods=['GET'])
def home():
    server_id = hash_ring.get_node(str(request.remote_addr))
    return jsonify({
        "message": f"Hello from {server_id}",
        "status": "successful"
    }), 200

# Endpoint /heartbeat
@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return "", 200

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
