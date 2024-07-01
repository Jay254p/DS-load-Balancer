import hashlib
import bisect
import logging

class ConsistentHashRing:
    def __init__(self, nodes=None, replicas=3, slots=512):
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
            key = self._hash(f"{node}:{i}")
            self.ring[key] = node
            bisect.insort(self.sorted_keys, key)
            logging.info(f"Added replica {i} for node {node} with key {key}")

    def remove_node(self, node):
        logging.info(f"Removing node: {node}")
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            if key in self.ring:
                del self.ring[key]
                self.sorted_keys.remove(key)
                logging.info(f"Removed replica {i} for node {node} with key {key}")

    def get_node(self, string_key):
        if not self.ring:
            logging.error("Hash ring is empty")
            return None
        key = self._hash(string_key)
        idx = bisect.bisect(self.sorted_keys, key) % len(self.sorted_keys)
        selected_node = self.ring[self.sorted_keys[idx]]
        logging.info(f"Key {string_key} (hashed to {key}) is mapped to node {selected_node}")
        return selected_node

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16) % self.slots

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    nodes = ["Server1", "Server2", "Server3"]
    ch_ring = ConsistentHashRing(nodes)

    print("Consistent Hash Ring:")
    for i in range(10):
        print(f"Request {i} is mapped to {ch_ring.get_node(str(i))}")
