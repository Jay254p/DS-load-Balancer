import hashlib
import bisect

class ConsistentHashRing:
    def __init__(self, nodes=None, replicas=9, slots=512):
        self.replicas = replicas
        self.slots = slots
        self.ring = dict()
        self.sorted_keys = []
        self.nodes = nodes

        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node):
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            self.ring[key] = node
            bisect.insort(self.sorted_keys, key)

    def remove_node(self, node):
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            if key in self.ring:
                del self.ring[key]
                self.sorted_keys.remove(key)

    def get_node(self, string_key):
        if not self.ring:
            return None
        key = self._hash(string_key)
        idx = bisect.bisect(self.sorted_keys, key)
        idx = idx % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16) % self.slots

# Example usage:
if __name__ == "__main__":
    nodes = ["Server1", "Server2", "Server3"]
    ch_ring = ConsistentHashRing(nodes)

    print("Consistent Hash Ring:")
    for i in range(10):
        print(f"Request {i} is mapped to {ch_ring.get_node(str(i))}")
