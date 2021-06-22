import datetime
import random
from hashlib import sha256 as sha256
from datetime import datetime


class Transaction:
    def __init__(self, fromAddress, toAddress, amount):
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount

    def __str__(self):
        return self.fromAddress + self.toAddress, self.amount


class Block:
    def __init__(self, timestamp, transactions, previousHash):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previousHash = previousHash
        # nonce is used in mineBlock function, increments its value by 1 everytime it function loops to give a different
        # hash everytime
        self.nonce = 0
        # hash value is calculate by custom has function, to avoid randomization of __hash__ on recalculation
        self.hash = self.calculateHash()

    # def __eq__(self, other):
    #    return self.data, self.index, self.timestamp == other.data, other.index, other.timestamp
    #
    # def __hash__(self):
    #    value = hash((self.data, self.index, self.timestamp))
    #    return value

    # using SHA256 from hashlib
    def calculateHash(self):
        return sha256((str(self.transactions) + str(self.timestamp) +
                       str(self.nonce)).encode('utf-8')).hexdigest()

    # to mine a block aka- add a new block to the blockchain, hash of a block should have all 0 at [0:difficulty]
    # indices.
    # AKA PRoOF OF WORK
    def mineBlock(self, difficulty):
        l = "0" * difficulty
        print("hash is ....")
        while self.hash[0: difficulty] != l:
            # nonce is incremented by 1 for calculateHash() to give a new hash everytime.
            self.nonce += 1
            self.hash = self.calculateHash()
        # time used to time the mining time of a block
        # now = datetime.now()
        # current_time = now.strftime("%H:%M:%S")
        # print("Current Time =", current_time)
        print(self.hash)
        # print(self.nonce)

    def __str__(self):
        return "timestamp: %s; " % self.timestamp + \
               "hash: %s; " % self.hash + "previousHash: %s; " % self.previousHash


class blockChain:
    def __init__(self):
        self.chain = []
        self.difficulty = 5
        self.pendingTransactions = []
        self.miningReward = 150

    # def createGenesisBlock(self):
    #    return Block("01/01/2021", "Genisis Block", 0)

    def getLatestBlock(self):
        return self.chain[-1]

    def minePendingTransactions(self, miningRewardAddress):
        block = Block("12/12/20021", self.pendingTransactions, 0)
        block.mineBlock(self.difficulty)
        print("block mined successfully")
        print()
        self.chain.append(block)
        self.pendingTransactions = [Transaction(0, miningRewardAddress, self.miningReward)]

    def addTransaction(self, transaction):
        self.pendingTransactions.append(transaction)

    def getBalanceOfAddress(self, address):
        balance = 0
        for block in self.chain:
            for trans in block.transactions:
                if trans.fromAddress == address:
                    balance -= trans.amount
                if trans.toAddress == address:
                    balance += trans.amount
        return balance

    #    def addNewBlock(self, newBlock):
    #        newBlock.previousHash = self.getLatestBlock().hash
    #        newBlock.mineBlock(self.difficulty)
    #        self.chain.append(newBlock)

    def isChainValid(self):
        for k in range(len(self.chain)):
            if k != 0:
                currentBlock = self.chain[k]
                prevBlock = self.chain[k - 1]
                if not currentBlock.hasValidTransactions():
                    return False
                if currentBlock.hash != currentBlock.calculateHash():
                    return False
                if currentBlock.previousHash != prevBlock.hash:
                    return False
        return True

    def p(self):
        for k in self.chain:
            print(k)
            print()


coin = blockChain()
coin.addTransaction(Transaction('address1', 'address2', '1'))

print("Strating miner")
coin.minePendingTransactions("Shrey's wallet")
coin.minePendingTransactions("Shrey's wallet")
coin.minePendingTransactions("Shrey's wallet")


print("balance of Shrey's wallet: %d" % coin.getBalanceOfAddress("Shrey's wallet"))
print("balance of Tom's Wallet: %d" % coin.getBalanceOfAddress("Tom's Wallet"))
