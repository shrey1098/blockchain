from ecdsa import SigningKey
from blockchain import blockChain, Transaction

myKey = SigningKey.from_pem("key goes here")
walletKey = myKey.verifying_key

coin = blockChain()

tx1 = Transaction(fromAddress=walletKey, toAddress='public key goes here', amount=10)
tx1.signTransaction(myKey)
coin.addTransaction(tx1)

coin.minePendingTransactions(walletKey)

tx2 = Transaction(fromAddress=walletKey, toAddress='public key goes here', amount=100)
tx2.signTransaction(myKey)
coin.addTransaction(tx2)

coin.minePendingTransactions(walletKey)

print(coin.getBalanceOfAddress(walletKey))
print(coin.isChainValid())
