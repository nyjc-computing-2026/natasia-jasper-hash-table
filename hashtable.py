

def _hash_key(key: str, p: int = 53) -> int:
    """Hashes the key using the rolling polynomial algorithm.

    Arguments:
    - key: str
      The key to be hashed.
    - p: int
      A prime number used for the rolling polynomial algorithm

    Returns:
    - the hashed location (int)
    """
    total = 0
    for i, char in enumerate(key):
        total += ord(char) * p**i
    return total


class HashTable:
    """A hashtable without collision resolution.

    Arguments:
    - size: int
      The number of slots that the hash table is initialised with

    Attributes:
    - size: int
      The number of slots that the hash table has
    - length: int
      The number of records contained in the hash table
    """

    def __init__(self, size: int):
        self.size = size
        self.length = 0
        self._data = [None] * size

    def __repr__(self) -> str:
        return f"HashTable(size={self.size})"

    def setitem(self, key: str, value: dict) -> None:
        """Stores key and value in the hash table.

        If the key already exists in the hash table, the existing value
        is overwritten.
        """
        index = _hash_key(key) % self.size
        self._data[index] = value 

    def getitem(self, key: str) -> dict:
        """Retrieves the value associated with key, and returns it.

        If the key does not exist, a KeyError is raised.
        """
        index = _hash_key(key) % self.size
        if self._data[index] is None:
            raise KeyError(f"key {key} not found")
        return self._data[index]

    def delitem(self, key: str) -> None:
        """Deletes the key and its associated value from the hash table.

        If the key does not exist, a KeyError is raised.
        """
        index = _hash_key(key) % self.size
        if self._data[index] is None:
            raise KeyError(f"key {key} not found")
        self._data[index] = None


class HashTableLinearProbing(HashTable):
    """A hashtable that implements collision resolution using
    linear probing.

    Arguments:
    - size: int
      The number of slots that the hash table is initialised with
    """

    def __init__(self, size: int):
        super().__init__(size)
        # Add your code here

    def __repr__(self) -> str:
        return f"HashTableLinearProbing(size={self.size})"

    def setitem(self, key: str, value: dict) -> None:
        """Stores key and value in the hash table.

        If the key already exists in the hash table, the existing value
        is overwritten.
        """
        index = _hash_key(key) % self.size

        for _ in range(self.size):
            if self._data[index] is None:
                self._data[index] = (key, value)
                return
            else:
                existing_key, existing_value = self._data
                if key == existing_key:
                    self._data[index] = (key, value)
                    return
                else:
                    index = (index + 1) % self.size
        raise RuntimeError("hash table is full")

    def getitem(self, key: str) -> dict:
        """Retrieves the value associated with key, and returns it.

        If the key does not exist, a KeyError is raised.
        """
        index = _hash_key(key) % self.size

        for _ in range(self.size):
            if self._data[index] is None:
                raise KeyError(f"key {key} not found") 
            # which is a problem bc once it finds a None it will raise 
            # a key error and return whereas the item may be at the bottom
            else:
                existing_key, existing_value = self._data
                if key == existing_key:
                    return existing_value
                else:
                    index = (index + 1) % self.size
        raise RuntimeError(f"key {key} not found")

    def delitem(self, key: str) -> None:
        """Deletes the key and its associated value from the hash table.

        If the key does not exist, a KeyError is raised.
        """
        index = _hash_key(key) % self.size

        for _ in range(self.size):
            if self._data[index] is None:
                raise KeyError(f"key {key} not found")
            else:
                existing_key, existing_value = self._data
                if key == existing_key:
                    # Erasing this key-value pair could affect probing
                    # for subsequent key-value pairs
                    # Need a strategy to handle this, e.g.
                    # re-insert affected key-value pairs, or insert tombstone
                    self._data[index] = None
                else:
                    index = (index + 1) % self.size
        raise RuntimeError(f"key {key} not found")

class Node:
    def __init__(self, key: str, value: dict):
        self.key = key
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def setitem(self, key: str, value: dict) -> None:
        #if key doesn't exist
        if self.head is None:
            self.head = Node(key, value)
        
        current = self.head

        # checks if key already exists
        while current is not None:
            if current.key == key:
                current.value = value
                return
            current = current.next
    
    def getkey(self, key: str) -> dict:
        if self.head is None:
            raise KeyError(f"key {key} not found")
        
        current = self.head

        while (
            current is not None
            and current.key != key
        ):
            current = current.next
            if current.key == key:
                return current.value
            raise KeyError(f"key {key} not found")
    
    def delkey(self, key: str):
        if self.head is None:
            raise KeyError(f"key {key} not found")
        
        if self.head.key == key:
            self.head = None
        
        previous = self.head

        while (
            previous.next is not None
            and previous.next.key != key
        ):
            previous = self.head
            current = previous.next
            if current.key == key:
                previous.next = current.next
            
        raise KeyError(f"key {key} not found")

class HashTableSeparateChaining(HashTable):
    """A hashtable that implements collision resolution using
    separate chaining.

    Arguments:
    - size: int
      The number of slots that the hash table is initialised with
    """

    def __init__(self, size: int):
        super().__init__(size)
        for i in range(len(self._data)):
            self._data[i] = LinkedList()

    def __repr__(self) -> str:
        return f"HashTableLinearProbing(size={self.size})"

    def setitem(self, key: str, value: dict) -> None:
        """Stores key and value in the hash table.

        If the key already exists in the hash table, the existing value
        is overwritten.
        """
        index = _hash_key(key)
        self._data[index].setitem(key, value)

    def getitem(self, key: str) -> dict:
        """Retrieves the value associated with key, and returns it.

        If the key does not exist, a KeyError is raised.
        """
        index = _hash_key(key)
        self._data[index].getkey(key)

    def delitem(self, key: str) -> None:
        """Deletes the key and its associated value from the hash table.

        If the key does not exist, a KeyError is raised.
        """
        index = _hash_key(key)
        self._data[index].delkey(key)
