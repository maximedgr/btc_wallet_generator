import hashlib
import main
import verifyPhrase
from ecdsa import ECDH, SECP256k1, SigningKey, VerifyingKey
import hmac
from typing import List

# Child key generation
#FUNCTIONS

def child_key(private_key: bytes, public_key: bytes, chain_code: bytes, derivation_path: List[str]):
    if derivation_path[0] == "m":
        return child_key(private_key, public_key, chain_code, derivation_path[1:])
    if len(derivation_path) == 1:
        return private_key, public_key, chain_code
    index = int(derivation_path[1])
    n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    hash = hmac.new(
        chain_code, b"\x00" + private_key + index.to_bytes(4, "big"), hashlib.sha512
    ).digest()
    chain_code_child = hash[32:]
    # tSomme de la clé privée et des 32 bytes du hash dans une nouvelle clée
    child_private_key = ((int.from_bytes(hash[:32], "big") + int.from_bytes(private_key, "big")) % n).to_bytes(32, "big")
    child_public_key = get_public_key(child_private_key)
    return child_key(child_private_key, child_public_key, chain_code_child, derivation_path[1:])

def get_public_key(private_key: bytes):
    signing_key = SigningKey.from_string(private_key, curve=SECP256k1, hashfunc=hashlib.sha256)
    ecdh = ECDH(curve = SECP256k1, private_key=signing_key)
    public_key: VerifyingKey = ecdh.get_public_key()
    return public_key.to_string()

def child_wallet_info(private, public, chain_code, derivation_path):
    print('Derivation path: {}'.format(derivation_path))
    print('Private key: {}'.format(private.hex()))
    print('Public address : {}'.format(public.hex()))
    print('Chain code: {}'.format(chain_code.hex()))

#MAIN function

def derivate_key():
    phrase = input("Please type your 12 words passPhrase : ")
    index_list = verifyPhrase.getFileWords()
    intPhrase = verifyPhrase.wordToInt(phrase, index_list)
    binPhrase = verifyPhrase.intToBin(intPhrase)
    m_private_k, m_public_k, chain_code= main.wallet_info(verifyPhrase.verifyChecksum(binPhrase))
    derivation_path=input("\nEnter derivation path (ex : m/0/1/2/3 4) : \n")
    m_private_k, m_public_k, chain_code=child_key(m_private_k, m_public_k, chain_code,derivation_path.split('/'))
    print("\nWallet infos : ")
    child_wallet_info(m_private_k,m_public_k,chain_code,derivation_path)
    