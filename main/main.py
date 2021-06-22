from ecdsa import SigningKey
from blockchain import blockChain, Transaction

myKey = SigningKey.from_pem(b'-----BEGIN EC PRIVATE KEY-----\nMHQCAQEEIIjiERxAewTApOl2QAnFHgSWxKYIOqp/j5ulvPl'
                            b'/jBgNoAcGBSuBBAAK\noUQDQgAEZgYtlqo5oXj8xI+YeYRfPwEqqzFgDlodQ3/wuCEMG2flFSEmlc1EVcjN'
                            b'\ng1wFDPSC61g62ixhrWQ+AgKHErW7Ug==\n-----END EC PRIVATE KEY-----\n')
walletKey = myKey.verifying_key

coin = blockChain()

tx1 = Transaction(walletKey, 'public key goes here', 10)
tx1.signTransaction(myKey)

coin.addTransaction(tx1)

coin.minePendingTransactions(walletKey)

tx2 = Transaction(walletKey, 'public key goes here', 100)
tx2.signTransaction(myKey)

coin.addTransaction(tx2)

coin.minePendingTransactions(walletKey)

print(coin.getBalanceOfAddress(walletKey))
print(coin.isChainValid())
