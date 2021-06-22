import datetime
from hashlib import sha256 as sha256
from datetime import datetime



# object transaction is inside a block.

# A block can have many transaction objects, the list 'pending transactions' # contains all un-mined transactions which
# are then all added to a block when a block is mined

class Transaction:
    """
    from and to addresses will be the public key of a wallet, and in case of a mining reward transaction fromAddress
    will be 'System'.
    
    Signature:  is initially set to 0 for the transaction, transaction is signed when signTransaction(signingKey) is 
    called.
    """
    def __init__(self, fromAddress, toAddress, amount):
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount
        self.signature = 0

    def calculateHash(self):
        # returns hash in bytes for the purpose of signing
        return bytes(sha256((str(self.fromAddress) + str(self.toAddress) +
                             str(self.amount)).encode('utf-8')).hexdigest(), 'utf-8')

    def signTransaction(self, signingKey):
        """
        signingKey: parameter is passed as ecdsa.SigningKey.from_pem(key goes here). myKey variable in main/main.py
        shows the usage. myKey is the Private key and walletKey is the public key
        The keys are saved locally in format provided by the method .to_pem() in the ecdsa library. Same private key is
        passed in the above mentioned parameter.
        usage in main.py: .from_pem() converts the into the SigningKey object from a string generated from .to_pem()
        """
        if signingKey.verifying_key != self.fromAddress:
            # verifying_key object is the public address for private key
            raise PermissionError('You cannot sign transactions for other wallets')
        hashTx = self.calculateHash()
        sig = signingKey.sign(hashTx)
        # sign method inbuilt inside ecdsa. key.sign(message), message has to be in bytes.
        self.signature = sig

    def isValid(self):
        """
        Checks if transaction is valid or not.
        if from address is "System" means the transaction is a reward transaction.
        the rest of the function check is the signature exists or not and if it does .verify function inbuilt of ecdsa
        is used to verify whether the transaction's hash is signed by the from address or not.
        """
        if self.fromAddress == "System":
            return True
        if not self.signature or len(self.signature) == 0:
            return TypeError('No Signature in this transaction')
        publicKey = self.fromAddress
        return publicKey.verify(self.signature, self.calculateHash())

    def __str__(self):
        return self.fromAddress + self.toAddress, self.amount, self.signature


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
        # no need to convert hash of the block to bytes as this need not be signed
        return sha256((str(self.transactions) + str(self.timestamp) +
                       str(self.nonce)).encode('utf-8')).hexdigest()

    # to mine a block aka- add a new block to the blockchain, hash of a block should have all 0 at [0:difficulty]
    # indices.
    # AKA PROOF OF WORK
    def mineBlock(self, difficulty):
        difficult = "0" * difficulty
        # difficulty = 000.. (number of 0's depends on the difficulty
        # this is what makes generating a hash time consuming and energy consuming.(AKA mining)
        print("hash is ....")
        while self.hash[0: difficulty] != difficult:
            # nonce is incremented by 1 for calculateHash() to give a new hash everytime.
            self.nonce += 1
            self.hash = self.calculateHash()
        # time used to time the mining time of a block
        # now = datetime.now()
        # current_time = now.strftime("%H:%M:%S")
        # print("Current Time =", current_time)
        print(self.hash)
        # print(self.nonce)

    def hasValidTransactions(self):
        # every transaction inside the block is check for validity through .isValid() in Transaction.
        for tx in self.transactions:
            if not tx.isValid():
                return False
        return True

    def __str__(self):
        return "timestamp: %s; " % self.timestamp + \
               "hash: %s; " % self.hash + "previousHash: %s; " % self.previousHash


class blockChain:
    """
    chain: a list of blocks. A block is only appended when it is mined
    difficulty: difficulty is used while mining a block, higher the difficulty more time it will take to mine the block
                see usage in Block.mineBlock().
    pendingTransactions: when a transaction has occurred it is added to this list as Transaction object, when a block is
                            mined all the transactions in this list as added to the transactions of the block as a list,
                            and this list is set to empty again for new transactions.

    """
    def __init__(self):
        self.chain = []
        self.difficulty = 2
        self.pendingTransactions = []
        self.miningReward = 150

    # def createGenesisBlock(self):
    #    return Block("01/01/2021", "Genesis Block", 0)

    def getLatestBlock(self):
        # returns the hash of the last block for previous hash of the new block to be added
        if len(self.chain) == 0:
            return 0
        else:
            return self.chain[-1].hash

    def minePendingTransactions(self, miningRewardAddress):
        """
        miningRewardAddress is passed. As when the mining is of the block is complete the mining reward transaction
        is added to the pending transactions.
        """
        # a new block instance is created with transaction= pendingTransactions
        block = Block(datetime.today(), self.pendingTransactions, self.getLatestBlock())
        block.mineBlock(self.difficulty)
        # mineBlock is called here.
        print("block mined successfully")
        print()
        self.chain.append(block)
        # reward transaction is added to pending transactions here, will be mined in the next block.
        # when the next block is mined only then the reward transaction will be processed and balance will increase
        self.pendingTransactions = [Transaction(fromAddress="System", toAddress=miningRewardAddress,
                                                amount=self.miningReward)]

    def addTransaction(self, transaction):
        """adds a transaction to pending transaction list. This is for regular transactions
         i.e. non reward transactions"""
        if not transaction.fromAddress or not transaction.toAddress:
            # if for or to address dont exists, Permission error
            raise PermissionError('transaction must include from and to address')
        if not transaction.isValid():
            # validity of transaction is checked
            raise PermissionError('cannot add invalid transactions to chain')
        # if both tests passed transaction is added to pending transactions
        self.pendingTransactions.append(transaction)

    def getBalanceOfAddress(self, address):
        """
        gets balance of a given address(public key), by iterating over all transactions in each block one by one
        and adding the amount of a Transaction to balance where address is toAddress i.e coins received, and subtracting
        the amount of a Transaction from balance where address is fromAddress i.e coins sent.
        """
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
        # checks for validity of chain
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
        # debug function to print each block in the chain
        for k in self.chain:
            print(k)
            print()
