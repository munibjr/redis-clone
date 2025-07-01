import socket
import threading
import pickle
from typing import Dict, Any

class RedisClone:
    def __init__(self, port=6379):
        self.port = port
        self.data: Dict[str, Any] = {}
        self.lock = threading.Lock()
        
    def set(self, key: str, value: Any):
        with self.lock:
            self.data[key] = value
            
    def get(self, key: str) -> Any:
        with self.lock:
            return self.data.get(key)
    
    def delete(self, key: str):
        with self.lock:
            if key in self.data:
                del self.data[key]
    
    def incr(self, key: str, delta: int = 1):
        with self.lock:
            self.data[key] = self.data.get(key, 0) + delta
            return self.data[key]
    
    def lpush(self, key: str, value: Any):
        with self.lock:
            if key not in self.data:
                self.data[key] = []
            if isinstance(self.data[key], list):
                self.data[key].insert(0, value)
    
    def save(self, filename='dump.rdb'):
        with self.lock:
            with open(filename, 'wb') as f:
                pickle.dump(self.data, f)
    
    def load(self, filename='dump.rdb'):
        try:
            with self.lock:
                with open(filename, 'rb') as f:
                    self.data = pickle.load(f)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    redis = RedisClone()
    redis.load()
    print(f"Redis Clone running on port 6379")
