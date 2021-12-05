from hashlib import sha256
import json
from . import transaction
class Block:
    def __init__(self, timestamp, transactions, prev = ""):
        self.timestamp = timestamp
        self.transactions = transactions
        self.prev = prev
        self.Nonce = 0
        self.hash = self.calculateHash()



    def calculateHash(self):
        return sha256((str(self.timestamp) + str(self.transactions) + str(self.Nonce)).encode()).hexdigest()
    def mineBlock(self, difficulty):
        tempHash = self.hash[0: difficulty+1]

        while(tempHash != ("0"*difficulty)):
            self.Nonce+=1
            self.hash = self.calculateHash()
            tempHash = self.hash[0: difficulty]

        print("Block Mined")
    def addTransaction(self, transaction):
        self.transactions.append(transaction)
