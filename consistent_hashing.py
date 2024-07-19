import hashlib
import bisect
import logging

class ConsistentHashRing:
    def __init__(self, nodes=None, replicas=9, slots=512):
        self.replicas = replicas
        self.slots = slots
        self.ring = dict()
        self.sorted_keys = []
        self.nodes = nodes or []

        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node):
        logging.info(f"Adding node: {node}")
        for i in range(self.replicas):
            key = self._hash_virtual_server(node, i)
            self.ring[key] = node
            bisect.insort(self.sorted_keys, key)
            logging.info(f"Added replica {i} for node {node} with key {key}")

    def remove_node(self, node):
        logging.info(f"Removing node: {node}")
        for i in range(self.replicas):
            key = self._hash_virtual_server(node, i)
            if key in self.ring:
                del self.ring[key]
                self.sorted_keys.remove(key)
                logging.info(f"Removed replica {i} for node {node} with key {key}")

    def get_node(self, string_key):
        if not self.ring:
            logging.error("Hash ring is empty")
            return None
        key = self._hash_request(string_key)
        idx = bisect.bisect(self.sorted_keys, key) % len(self.sorted_keys)
        selected_node = self.ring[self.sorted_keys[idx]]
        logging.info(f"Key {string_key} (hashed to {key}) is mapped to node {selected_node}")
        logging.info(f"Sorted keys: {self.sorted_keys}")
        return selected_node

    def _hash_request(self, key):
        # Modify this method to use the provided function H(i)
        i = int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)
        hash_val = i + 2 * i + 17
        hash_val = hash_val % self.slots
        logging.info(f"Request key {key} hashed to {hash_val}")
        return hash_val

    def _hash_virtual_server(self, node, replica_index):
        # Modify this method to use the provided function Φ(i, j)
        key = f"{node}:{replica_index}"
        i = int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)
        j = replica_index
        hash_val = i + j + 2 * j + 25
        hash_val = hash_val % self.slots
        logging.info(f"Virtual server key {key} hashed to {hash_val}")
        return hash_val
