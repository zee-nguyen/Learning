"""
Implement a simple caching mechanism in Python using a dictionary. The cache should support getting and setting values and should use a fixed size (e.g., 3 items). If the cache exceeds this size, it should evict the oldest item.
"""

from collections import OrderedDict


class LRUCache:
    def __init__(self, size):
        self.cache = OrderedDict()
        self.size = size

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def set(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.size:
            # remove the first item (least recently used)
            self.cache.popitem(last=False)
        self.cache[key] = value


cache = LRUCache(3)
cache.set("a", 1)
cache.set("b", 2)
cache.set("c", 3)
print([(k, v) for k, v in cache.cache.items()])
print(cache.get("a"))  # 1
print([(k, v) for k, v in cache.cache.items()])
print(cache.get("b"))  # 2
cache.set("d", 4)
print([(k, v) for k, v in cache.cache.items()])
print(cache.get("b"))  # 2
print(cache.get("c"))  # None
