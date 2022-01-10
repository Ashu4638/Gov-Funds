from . import Block
from datetime import datetime
from . import transaction


class Blockchain:
    def __init__(self, fund, name):
        self.fund = fund
        self.name = name
        self.chain = [self.createGenesisBlock()]
        self.difficulty = 2
        self.pendingtransactions = []
        self.validity = self.isChainValid()

    def createGenesisBlock(self):
        return Block.Block(datetime.now(), [transaction.Transaction(self.name, "None", 0)], "0")

    def getLatestBlock(self):
        return self.chain[-1].hash

    def minependingTransacrions(self):
        block = Block.Block(datetime.now(), self.pendingtransactions, self.getLatestBlock())
        block.mineBlock(self.difficulty)
        for transaction in self.pendingtransactions:
            self.fund -= transaction.amount
        print("Block Mined !")
        self.chain.append(block)
        self.pendingtransactions = []


    def createTransaction(self, transaction):
        self.pendingtransactions.append(transaction)

    def getBalanceofAdd(self, address):
        balance = 0

        for block in range(1, len(self.chain)):
            for transaction in self.chain[block].transactions:
                if (transaction.fromAdd == address):
                    balance -= transaction.amount
                if (transaction.toAdd == address):
                    balance += transaction.amount

        return balance

    def isChainValid(self):
        for i in range(1, len(self.chain)):
            currBlock = self.chain[i]
            prevBlock = self.chain[i - 1]
            if (currBlock.hash != currBlock.calculateHash()):
                return False
            if (currBlock.prev != prevBlock.hash):
                return False
        return True
