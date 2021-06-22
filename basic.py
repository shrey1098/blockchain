import datetime
import random
from hashlib import sha256 as sha256
from datetime import datetime


class Block:
    def __init__(self, index, timestamp, data, previousHash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
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
        return sha256((str(self.index) + str(self.data) + str(self.timestamp) +
                       str(self.nonce)).encode('utf-8')).hexdigest()

    # to mine a block aka- add a new block to the blockchain, hash of a block should have all 0 at [0:difficulty]
    # indices.
    def mineBlock(self, difficulty):
        x = "0" * difficulty
        print("hash is ....")
        while self.hash[0: difficulty] != x:
            # nonce is incremented by 1 for calculateHash() to give a new hash everytime.
            self.nonce += 1
            self.hash = self.calculateHash()
        # time used to time the mining time of a block
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        print(self.hash)
        print(self.nonce)
        print()

    def __str__(self):
        return " index: %d; " % self.index + "timestamp: %s; " % self.timestamp + "data: %d; " % self.data + \
               "hash: %s; " % self.hash + "previousHash: %s; " % self.previousHash


class blockChain:
    def __init__(self):
        self.chain = [self.createGenesisBlock()]
        self.difficulty = 9
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("start_time =", current_time)

    @staticmethod
    def createGenesisBlock():
        return Block(0, "01/01/2021", 100, 0)

    def getLatestBlock(self):
        return self.chain[-1]

    def addNewBlock(self, newBlock):
        newBlock.index = self.getLatestBlock().index + 1
        newBlock.previousHash = self.getLatestBlock().hash
        newBlock.mineBlock(self.difficulty)
        self.chain.append(newBlock)

    def isChainValid(self):
        for k in range(len(self.chain)):
            if k != 0:
                currentBlock = self.chain[k]
                prevBlock = self.chain[k - 1]

                if currentBlock.hash != currentBlock.calculateHash():
                    return False
                if currentBlock.previousHash != prevBlock.hash:
                    return False
        return True

    def p(self):
        for k in self.chain:
            print(k)
            print()


x = blockChain()
for i in range(4):
    x.addNewBlock(
        Block(index=i + 1, timestamp=datetime.now(), data=random.randint(1, 80000), previousHash=0))

x.p()