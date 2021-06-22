from ecdsa import SigningKey, SECP256k1

privateKey = SigningKey.generate(curve=SECP256k1)
publicKey = privateKey.verifying_key
privatePEM = privateKey.to_pem()
publicPEM = publicKey.to_pem()
print(publicPEM)
print(privatePEM)
