#!/usr/bin/env python3
import binascii
import hashlib
import codecs
from ecdsa import ECDH, SECP256k1, SigningKey, VerifyingKey
import secrets, hashlib
import derivation
import verifyPhrase

BITS = 128

####### Functions

#Extraction des mots pour la phrase mnemonic - BIP39
def getFileWords():
    index_list = []
    with open("bip-39Words.txt", "r", encoding='utf-8') as file:
        for word in file.readlines():
            index_list.append(word.strip())
    return index_list

#Génération de la phrase mnemonic
def getMnemonicPhrase(bin_result, index_list):
    wordlist = []
    for i in range(len(bin_result) // 11):
        index = int(bin_result[i*11 : (i+1)*11], 2)
        wordlist.append(index_list[index])
    return wordlist

def from_bitstring_to_byte(bitstring, size=32):
    number = int(bitstring, 2)
    return number.to_bytes(size, byteorder='big')

#Génération de la master private key - BIP43/44
def master_chaincode(bin_seed):
    seed = from_bitstring_to_byte(bin_seed, 16)

    # Get master private key and chaincode
    sha = hashlib.sha512(seed).digest()
    private_key = sha[:32]
    chain_code = sha[32:]
    # Get master public key
    public_key = get_public_key(private_key)
    return private_key, public_key, chain_code

def get_public_key(private_key: bytes):
    signing_key = SigningKey.from_string(private_key, curve=SECP256k1, hashfunc=hashlib.sha256)
    ecdh = ECDH(curve = SECP256k1, private_key=signing_key)
    public_key: VerifyingKey = ecdh.get_public_key()
    return public_key.to_string()

def wallet_info(seed):
    print("\n#########")
    m_private_k, m_public_k, chain_code = master_chaincode(seed)
    print("\nMaster Private key : ",end='')
    print(m_private_k.hex())
    print("\nMaster Chain Code : ",end='')
    print(chain_code.hex())
    print("\nMaster Public Key : ",end='')
    print(m_public_k.hex())
    print("\n#########")
    return m_private_k, m_public_k, chain_code


def generate_wallet():

    #Génération de generated entropie et du hash associé    
    print("###### Génération d'un wallet BTC : ######\n\n")
    entropy_bytes = secrets.token_bytes(16)
    #print('Entropy: '+ str(entropy_bytes))
    hex_entropy = entropy_bytes.hex()
    #print("\nHex_entropy : \n" + hex_entropy)

    #Hash via SHA256 de l'entropie
    hashed_entropy = hashlib.sha256(entropy_bytes).hexdigest()
    #print("\nHashed_entropy : \n" + hashed_entropy)
    #print('\n')

    #Conversion en binaire et ajout checksum à l'entropie
    withoutChecksum = bin(int(hex_entropy, 16))[2:].zfill(BITS)
    bin_result = (
        withoutChecksum
        + bin(int(hashed_entropy, 16))[2:].zfill(BITS)[:4]
    )
    #print('\nBin result: ' + str(bin_result))

    #Création de la phrase mnémonic associée à la seed
    index_list = getFileWords()
    wordlist = getMnemonicPhrase(bin_result, index_list)

    phrase = " ".join(wordlist) 
    print("Mnemonic seed phrase :  ",end='')
    print(phrase)
    #Master keys et Chain Code
    wallet_info(withoutChecksum)


    #Fin


##### Menu

menu_options = {
    1: 'Generate BTC wallet',
    2: 'Verify Seed',
    3: 'Get child address with derivation path',
    4: 'Exit',
}

def print_menu():
    print("\n\n#########\n")
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def option1():
     print('Handle option : \'Generate BTC wallet\'')
     generate_wallet()

def option2():
     print('Handle option : \'Verify Seed\'')
     verifyPhrase.verify_seed()

def option3():
     print('Handle option : \'Get child address with derivation path\'')
     derivation.derivate_key()

##### Main

if __name__=='__main__':
    print("\n\nBTC Wallet Managment MENU :")
    looping=True
    while(looping):
        print_menu()
        option = ''
        try:
            option = int(input('\nEnter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        #Check what choice was entered and act accordingly
        if option == 1:
           option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            print('\nEnd...\n')
            looping=False
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')





