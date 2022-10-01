#!/usr/bin/env python3
import binascii
import hashlib
import base58
import codecs
import ecdsa
import secrets, hashlib
from turtle import right

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

#Génération de la master private key - BIP43/44
def master_private(root_seed_bytes):
    hmac_seed_out=bin(int(hashlib.sha512(root_seed_bytes).hexdigest(),16))
    print(len(hmac_seed_out))
    left_root=hmac_seed_out[2:258].zfill(256)
    master_chain_code=hmac_seed_out[258:].zfill(256)
    print(type(left_root))
    print(type(master_chain_code))
    return left_root,master_chain_code

def generate_wallet():

    #Génération de generated entropie et du hash associé    
    print("###### Génération d'un wallet BTC : ######\n\n")
    entropy_bytes = secrets.token_bytes(16)
    print('Entropy: '+ str(entropy_bytes))
    hex_entropy = entropy_bytes.hex()
    print("\nHex_entropy : \n" + hex_entropy)

    #Hash via SHA256 de l'entropie
    hashed_entropy = hashlib.sha256(entropy_bytes).hexdigest()
    print("\nHashed_entropy : \n" + hashed_entropy)
    print('\n')

    #Conversion en binaire et ajout checksum à l'entropie
    bin_result = (
        bin(int(hex_entropy, 16))[2:].zfill(BITS)
        + bin(int(hashed_entropy, 16))[2:].zfill(BITS)[:4]
    )
    print('\nBin result: ' + str(bin_result))

    #Création de la phrase mnémonic associée à la seed
    index_list = getFileWords()
    wordlist = getMnemonicPhrase(bin_result, index_list)

    phrase = " ".join(wordlist) 
    print("Mnemonic seed phrase :  ",end='')
    print(phrase)

    #Master key et Chain Code
    m_private_k,chain_code = master_private(bytes([int(i) for i in bin_result]))
    print("\nMaster Private key : ",end='')
    print(hex(int(m_private_k)))
    print("\nMaster Chain Code : ",end='')
    print(hex(int(chain_code)))

    ### Master public key

    # Hex decoding the private key to bytes using codecs library
    private_key_bytes = codecs.decode(m_private_k, 'hex')
    print("\n\n")
    print(private_key_bytes)
    print("\n")
    # Generating a public key in bytes using SECP256k1 & ecdsa library
    public_key_raw = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    public_key_bytes = public_key_raw.to_string()
    # Hex encoding the public key from bytes
    public_key_hex = codecs.encode(public_key_bytes, 'hex')
    # Bitcoin public key begins with bytes 0x04 so we have to add the bytes at the start
    public_key = (b'04' + public_key_hex).decode("utf-8")
    print("\nMaster Public Key : ",end='')
    print(public_key)


    #Fin


##### Menu

menu_options = {
    1: 'Generate BTC wallet',
    2: 'Verify Seed',
    3: '?',
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
     print('Handle option : \'Option 3\'')

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





