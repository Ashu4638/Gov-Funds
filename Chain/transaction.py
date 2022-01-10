from hashlib import sha256
from datetime import datetime
class Transaction:
    def __init__(self, fromAdd, toAdd, amount):
        self.fromAdd = fromAdd
        self.toAdd = toAdd
        self.amount = amount
        self.timestamp = datetime.now()
        self.hash = self.calculateHash()
        self.status = "Requested"


    def calculateHash(self):
        return sha256((str(self.fromAdd) + str(self.toAdd) + str(self.amount)).encode()).hexdigest()


